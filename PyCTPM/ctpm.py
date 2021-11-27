# Python Chemical Thermodynamics for Process Modeling
# ----------------------------------------------------

# import packages/modules
import json
import os
# internals
import PyCTPM.core.constants as CONST
from PyCTPM.core import packageName, loadGeneralData
from PyCTPM.docs import ExtCoreClass, eosCoreClass, dUtilityClass


def main():
    """ 
    Python Chemical Thermodynamics for Process Modeling
    """
    print(packageName)


def thermo(propName, modelInput, unit="SI"):
    '''
    estimate thermodynamic properties
    args:
        propName: property name
        modelInput:
            compList: component list
            MoFr: mole fraction
            params: 
                pressure
                temperature
            unit: set unit (SI, cgs)
    '''
    # try/except
    try:
        # get primary info
        compList = modelInput.get("components")

        # check component list
        compListUnique = dUtilityClass.buildComponentList(compList)

        # check property list
        propNameCheck = dUtilityClass.checkAppPropList(propName)

        # load general data
        dataGeneral = loadGeneralData(compListUnique)

        # class init
        ExtCoreClassSet = ExtCoreClass(
            dataGeneral, compListUnique, propNameCheck, modelInput, unit)

        # cal
        res = ExtCoreClassSet.propSet()
        return res
    except Exception as e:
        raise


def eosExe(modelInput):
    """
        eos init
    """
    # print(f"modelInput {modelInput}")
    # eos method
    eosNameSet = modelInput['eos']
    print(f"eosNameSet: {eosNameSet}")
    # model input
    pressureSet = modelInput['pressure']
    print(f"pressureSet: {pressureSet}")
    temperatureSet = modelInput['temperature']
    print(f"temperatureSet: {temperatureSet}")
    componentsSet = modelInput['components']
    print(f"componentsSet: {componentsSet}")
    moleFractionSet = modelInput['moleFraction']
    print(f"moleFractionSet: {moleFractionSet}")

    # * init eos class
    _eosCoreClass = eosCoreClass(
        pressureSet, temperatureSet, componentsSet, eosNameSet, moleFractionSet)
    # select method
    selectEOS = {
        "PR": lambda: _eosCoreClass._eosPR()
    }

    # return
    return selectEOS.get(eosNameSet)()


#! test json
def showJson():
    appPath = "database\component.json"
    print(appPath)
    with open(appPath) as f:
        data = json.load(f)
        print(data)
    #  lookup
    res = data["payload"]
    print(res)
    return res


if __name__ == "__main__":
    main()
