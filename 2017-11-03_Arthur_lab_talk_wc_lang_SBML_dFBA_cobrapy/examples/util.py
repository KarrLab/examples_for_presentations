from libsbml import OperationReturnValue_toString

def wrap_libsbml(method, *args, returns_int=False):
  # Wrap a libsbml method so that errors in return code can be easily handled.
  args_str = ', '.join([str(a) for a in args])
  call_str = "method: {}; args: {}".format(method, args_str)

  try:
    ### Call libSBML ###
    rc = method(*tuple(args))
  except BaseException as error:
    raise LibSBMLError("Error '{}' in libsbml method call '{}'.".format(
      error, call_str))

  if rc == None:
    raise LibSBMLError("libsbml returned None executing '{}'.".format(call_str))
  elif type(rc) is int:

    # if `method` returns an int value, do not interpret rc as an error code
    if returns_int:
      return rc

    if rc == LIBSBML_OPERATION_SUCCESS:
      return rc
    else:
      error_code = OperationReturnValue_toString(rc)
      if error_code is None:
        warn("wrap_libsbml: unknown error {} returned by '{}'. \nIf an integer "
          "value is returned, avoid this warning with 'returns_int=True'".format(
          error_code, call_str))
        return rc
      else:
        raise LibSBMLError("LibSBML returned error '{}' when executing '{}'".format(
          error_code, call_str))
  else:
    # return data provided by libsbml method
    return rc

from libsbml import (LIBSBML_OPERATION_SUCCESS, UNIT_KIND_SECOND, UNIT_KIND_MOLE, UNIT_KIND_GRAM,
    UNIT_KIND_DIMENSIONLESS, OperationReturnValue_toString, SBMLNamespaces, SBMLDocument)

def init_sbml_model(sbml_document):
    # Create and initialize an SMBL model
    sbml_model = wrap_libsbml(sbml_document.createModel)
    fbc_model_plugin = wrap_libsbml(sbml_model.getPlugin, 'fbc')
    wrap_libsbml(fbc_model_plugin.setStrict, True)

    # Set some units
    wrap_libsbml(sbml_model.setTimeUnits, 'second')
    wrap_libsbml(sbml_model.setExtentUnits, 'mole')
    wrap_libsbml(sbml_model.setSubstanceUnits, 'mole')

    # Create a unit definition we will need later
    per_second = wrap_libsbml(sbml_model.createUnitDefinition)
    wrap_libsbml(per_second.setIdAttribute, 'per_second')
    add_sbml_unit(per_second, UNIT_KIND_SECOND, exponent=-1)
    # etc.

    mmol_per_gDW_per_hr = wrap_libsbml(sbml_model.createUnitDefinition)
    wrap_libsbml(mmol_per_gDW_per_hr.setIdAttribute, 'mmol_per_gDW_per_hr')
    add_sbml_unit(mmol_per_gDW_per_hr, UNIT_KIND_MOLE, scale=-3)
    add_sbml_unit(mmol_per_gDW_per_hr, UNIT_KIND_GRAM, exponent=-1)
    add_sbml_unit(mmol_per_gDW_per_hr, UNIT_KIND_SECOND, exponent=-1,
        multiplier=3600.0)

    dimensionless = wrap_libsbml(sbml_model.createUnitDefinition)
    wrap_libsbml(dimensionless.setIdAttribute, 'dimensionless_ud')
    add_sbml_unit(dimensionless, UNIT_KIND_DIMENSIONLESS)

    return sbml_model


def str_to_xmlstr(str):
    """ Convert a Python string to an XML string that can be stored as a Note in an SBML Document.

    Args:
        str (:obj:`str`): a string

    Returns:
        :obj:`str`: an XML string that can be stored as a Note in an SBML Document
    """
    # TODO: GET libsbml to do this XML crap, but none of the obvious methods work
    return "<p xmlns=\"http://www.w3.org/1999/xhtml\">{}</p>".format(str)
