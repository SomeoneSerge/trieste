# Copyright 2021 The Trieste Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This package contains examples of popular objective functions used in (Bayesian) optimization.
"""

from . import multi_objectives, utils
from .single_objectives import (
    ACKLEY_5_MINIMIZER,
    ACKLEY_5_MINIMUM,
    ACKLEY_5_SEARCH_SPACE,
    BEALE_MINIMIZER,
    BEALE_MINIMUM,
    BEALE_SEARCH_SPACE,
    BRANIN_MINIMIZERS,
    BRANIN_MINIMUM,
    BRANIN_SEARCH_SPACE,
    DROP_WAVE_MINIMIZER,
    DROP_WAVE_MINIMUM,
    DROP_WAVE_SEARCH_SPACE,
    EGGHOLDER_MINIMIZER,
    EGGHOLDER_MINIMUM,
    EGGHOLDER_SEARCH_SPACE,
    GRAMACY_LEE_MINIMIZER,
    GRAMACY_LEE_MINIMUM,
    GRAMACY_LEE_SEARCH_SPACE,
    GRIEWANK_5_MINIMIZER,
    GRIEWANK_5_MINIMUM,
    GRIEWANK_5_SEARCH_SPACE,
    HARTMANN_3_MINIMIZER,
    HARTMANN_3_MINIMUM,
    HARTMANN_3_SEARCH_SPACE,
    HARTMANN_6_MINIMIZER,
    HARTMANN_6_MINIMUM,
    HARTMANN_6_SEARCH_SPACE,
    LOGARITHMIC_GOLDSTEIN_PRICE_MINIMIZER,
    LOGARITHMIC_GOLDSTEIN_PRICE_MINIMUM,
    LOGARITHMIC_GOLDSTEIN_PRICE_SEARCH_SPACE,
    MICHALEWICZ_2_MINIMIZER,
    MICHALEWICZ_2_MINIMUM,
    MICHALEWICZ_2_SEARCH_SPACE,
    MICHALEWICZ_5_MINIMIZER,
    MICHALEWICZ_5_MINIMUM,
    MICHALEWICZ_5_SEARCH_SPACE,
    MICHALEWICZ_10_MINIMIZER,
    MICHALEWICZ_10_MINIMUM,
    MICHALEWICZ_10_SEARCH_SPACE,
    ROSENBROCK_4_MINIMIZER,
    ROSENBROCK_4_MINIMUM,
    ROSENBROCK_4_SEARCH_SPACE,
    SCALED_BRANIN_MINIMUM,
    SCHWEFEL_8_MINIMIZER,
    SCHWEFEL_8_MINIMUM,
    SCHWEFEL_8_SEARCH_SPACE,
    SHEKEL_4_MINIMIZER,
    SHEKEL_4_MINIMUM,
    SHEKEL_4_SEARCH_SPACE,
    SIMPLE_QUADRATIC_MINIMIZER,
    SIMPLE_QUADRATIC_MINIMUM,
    SIMPLE_QUADRATIC_SEARCH_SPACE,
    TRID_10_MINIMIZER,
    TRID_10_MINIMUM,
    TRID_10_SEARCH_SPACE,
    ackley_5,
    beale,
    branin,
    drop_wave,
    eggholder,
    gramacy_lee,
    griewank_5,
    hartmann_3,
    hartmann_6,
    logarithmic_goldstein_price,
    michalewicz,
    michalewicz_2,
    michalewicz_5,
    michalewicz_10,
    rosenbrock_4,
    scaled_branin,
    schwefel_8,
    shekel_4,
    simple_quadratic,
    trid,
    trid_10,
)
