import os
# os.environ["CUDA_VISIBLE_DEVICES"] = ""
import jug
import numpy as np
import tensorflow as tf
from trieste.objectives import (
    michalewicz_2,
    michalewicz_5,
    michalewicz_10,
    MICHALEWICZ_2_MINIMUM,
    MICHALEWICZ_2_SEARCH_SPACE,
    MICHALEWICZ_5_MINIMUM,
    MICHALEWICZ_5_SEARCH_SPACE,
    MICHALEWICZ_10_MINIMUM,
    MICHALEWICZ_10_SEARCH_SPACE,
    ackley_5,
    ACKLEY_5_MINIMUM,
    ACKLEY_5_SEARCH_SPACE,
    hartmann_6,
    HARTMANN_6_MINIMUM,
    HARTMANN_6_SEARCH_SPACE,
    rosenbrock_4,
    ROSENBROCK_4_MINIMUM,
    ROSENBROCK_4_SEARCH_SPACE,
    shekel_4,
    SHEKEL_4_MINIMUM,
    SHEKEL_4_SEARCH_SPACE
)
from trieste.objectives.utils import mk_observer
import trieste
from trieste.acquisition.rule import DiscreteThompsonSampling
import pandas as pd
import time
from exp_utils import (
    build_gi_dgp_model,
    build_gp_model,
    build_vanilla_dgp_model,
    test_ll_gi_dgp,
    test_ll_gp,
    test_ll_vanilla_dgp,
)

np.random.seed(1794)
tf.random.set_seed(1794)
tf.keras.backend.set_floatx("float64")

runs = 10


function_dict = {
    "michalewicz_2": [michalewicz_2, MICHALEWICZ_2_MINIMUM, MICHALEWICZ_2_SEARCH_SPACE],
    "michalewicz_5": [michalewicz_5, MICHALEWICZ_5_MINIMUM, MICHALEWICZ_5_SEARCH_SPACE],
    "michalewicz_10": [michalewicz_10, MICHALEWICZ_10_MINIMUM, MICHALEWICZ_10_SEARCH_SPACE],
    "hartmann": [hartmann_6, HARTMANN_6_MINIMUM, HARTMANN_6_SEARCH_SPACE],
    "ackley": [ackley_5, ACKLEY_5_MINIMUM, ACKLEY_5_SEARCH_SPACE],
    "rosenbrock": [rosenbrock_4, ROSENBROCK_4_MINIMUM, ROSENBROCK_4_SEARCH_SPACE],
    "shekel": [shekel_4, SHEKEL_4_MINIMUM, SHEKEL_4_SEARCH_SPACE]
}

model_dict = {
    "deep_gp": [build_vanilla_dgp_model, test_ll_vanilla_dgp, False, False],
    "gi_dgp": [build_gi_dgp_model, test_ll_gi_dgp, False, False],
    "gp": [build_gp_model, test_ll_gp, False, False],
    "deep_gp_ln": [build_vanilla_dgp_model, test_ll_vanilla_dgp, True, False],
    "gi_dgp_ln": [build_gi_dgp_model, test_ll_gi_dgp, True, False],
    "gp_ln": [build_gp_model, test_ll_gp, True, False],
    "deep_gp_rt": [build_vanilla_dgp_model, test_ll_vanilla_dgp, False, True],
    "gi_dgp_rt": [build_gi_dgp_model, test_ll_gi_dgp, False, True],
    "gp_rt": [build_gp_model, test_ll_gp, False, True],
    "deep_gp_ln_rt": [build_vanilla_dgp_model, test_ll_vanilla_dgp, True, True],
    "gi_dgp_ln_rt": [build_gi_dgp_model, test_ll_gi_dgp, True, True],
    "gp_ln_rt": [build_gp_model, test_ll_gp, True, True]
}


for function_key in function_dict:
    if not os.path.exists(os.path.join('results', function_key)):
        os.makedirs(os.path.join('results', function_key))

    function = function_dict[function_key][0]
    F_MINIMIZER = function_dict[function_key][1]

    search_space = function_dict[function_key][2]
    observer = mk_observer(function)

    bo = trieste.bayesian_optimizer.BayesianOptimizer(observer, search_space)
    acquisition_rule = DiscreteThompsonSampling(1000, 1)

    num_initial_points = 20
    num_acquisitions = 480
    num_evaluation_points = 1000
    for run in range(runs):

        @jug.TaskGenerator
        def run_bayes_opt(
                model_key,
                initial_data,
                ll_evaluation_data,
                search_space
        ):
            start_time = time.time()

            builder = model_dict[model_key][0]
            tester = model_dict[model_key][1]
            learn_noise = model_dict[model_key][2]
            retrain = model_dict[model_key][3]

            # Run Bayes Opt
            if retrain:
                num_acq_per_loop = 10
                num_loops = num_acquisitions // num_acq_per_loop

                current_dataset = initial_data

                for loop in range(num_loops):
                    model = builder(current_dataset, learn_noise=learn_noise,
                                    search_space=search_space)
                    result = bo.optimize(num_acq_per_loop, current_dataset, model,
                                             acquisition_rule=acquisition_rule, track_state=False)
                    current_dataset = result.try_get_final_dataset()
            else:
                model = builder(initial_data, learn_noise=learn_noise, search_space=search_space)

                result = bo.optimize(num_acquisitions, initial_data, model,
                                     acquisition_rule=acquisition_rule, track_state=False)

            # Get results
            result_dataset = result.try_get_final_dataset()
            result_model = result.try_get_final_model()

            result_query_points = result_dataset.query_points.numpy()
            result_observations = result_dataset.observations.numpy()

            result_arg_min_idx = tf.squeeze(tf.argmin(result_observations, axis=0))

            result_evaluation_ll = tester(ll_evaluation_data, result_model)

            pd.DataFrame(result_query_points).to_csv(
                'results/{}/{}_query_points_{}'.format(function_key, model_key, run))
            pd.DataFrame(result_observations).to_csv(
                'results/{}/{}_observations_{}'.format(function_key, model_key, run))
            pd.DataFrame(result_evaluation_ll).to_csv(
                'results/{}/{}_ood_ll_{}'.format(function_key, model_key, run))

            print(f"{model_key} observation "
                  f"{function_key} {run}: {result_observations[result_arg_min_idx, :]}")
            print(f"{model_key} OOD LL: {result_evaluation_ll}")
            print("Time: ", time.time() - start_time)

        ll_evaluation_points = search_space.sample_sobol(num_evaluation_points)
        ll_evaluation_data = observer(ll_evaluation_points)

        initial_query_points = search_space.sample_sobol(num_initial_points)
        initial_data = observer(initial_query_points)

        for model_key in model_dict:
            run_bayes_opt(model_key, initial_data, ll_evaluation_data, search_space)