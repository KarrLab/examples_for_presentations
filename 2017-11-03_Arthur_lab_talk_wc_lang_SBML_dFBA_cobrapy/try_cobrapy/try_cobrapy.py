'''
try cobrapy on wc-lang model

algorithm:
x use wc-lang to read model
dFBA:
    save concentrations to history
    x use wc-lang to write FBA submodel to SBML file
    x use cobrapy to read SBML file
    solve FBA submodel
    update concentrations after time interval
plot history
'''
from argparse import Namespace
from os import path
import tempfile
import cobra
import warnings
warnings.filterwarnings('ignore', message='', module='wc_lang.prepare')
from libsbml import writeSBMLToFile

from wc_lang.io import Reader
import wc_lang.sbml.io as sbml_io
from obj_model import utils
from wc_lang.prepare import PrepareModel

args = Namespace(end_time=1,
    time_step=1,
    test_submodel_id='Metabolism',
    wc_lang_model="example-model.xlsx")

MODEL_FILENAME = path.join(path.dirname(__file__), '../../..', 'wc_lang/tests/fixtures',
    args.wc_lang_model)
print('using:', MODEL_FILENAME)
model = Reader().run(MODEL_FILENAME)
PrepareModel(model).run()
submodel = utils.get_component_by_id(model.get_submodels(), args.test_submodel_id)
_, SBMLfile = tempfile.mkstemp()

def try_cobrapy(args):
    time = 0
    while time < args.end_time:
        print('time:', time)
        sbml_document = sbml_io.SBMLExchange.write_submodel(submodel)
        if not writeSBMLToFile(sbml_document, SBMLfile):
            raise ValueError("SBML document for submodel '{}' could not be written to '{}'.".format(
                args.test_submodel_id, SBMLfile))
        # cobra_model = cobra.io.read_sbml_model(SBMLfile)
        cobra_model = cobra.io.sbml3.read_sbml_model(SBMLfile)
        print('cobra_model', cobra_model)
        print('cobra_model', cobra_model._repr_html_())
        solution = cobra_model.optimize()
        print(solution)

        time += args.time_step

try_cobrapy(args)


