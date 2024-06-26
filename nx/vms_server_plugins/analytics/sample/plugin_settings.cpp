#include "plugin_settings.h"

namespace nx {
namespace vms_server_plugins {
namespace analytics {
namespace aol_object_detection {

	const std::string objectKeyList[NUM_OBJECTS] = {
		kAeroplaneObjectType,
		kBackpackObjectType,
		kBicycleObjectType,
		kBoatObjectType,
		kBusObjectType,
		kCarObjectType,
		kCatObjectType,
		kCellPhoneObjectType,
		kDogObjectType,
		kHandbagObjectType,
		kHorseObjectType,
		kMotorbikeObjectType,
		kPersonObjectType,
		kTrainObjectType,
		kTruckObjectType,
		
	};

	std::string objectNames[NUM_OBJECTS]={
		"aeroplane",
		"backpack",
		"bicycle",
		"boat",
		"bus",
		"car",
		"cat",
		"cell phone",
		"dog",
		"handbag",
		"horse",
		"motorbike",
		"person",
		"train",
		"truck"	
		
	};

	bool getObjectName(size_t index, std::string& objName)
	{
		if(index>=NUM_OBJECTS)
		{
			return false;
		}
		objName = objectNames[index];
		return true;
	}

	const std::string & getKeyByName(std::string objName)
	{
		
		for (size_t i = 0; i < NUM_OBJECTS; i++)
		{
			std::string obj = objectNames[i];
			if(obj==objName)
			{
				return objectKeyList[i];
			}
		}
		
		return kAeroplaneObjectType;
	}


	int getObjectNamesList(std::vector<std::string> &objectNamesList)
	{
		objectNamesList.clear();
		for (size_t i = 0; i < NUM_OBJECTS; i++)
		{
			objectNamesList.push_back(objectNames[i]);
			
		}
		
		return objectNamesList.size();
	}

	int getObjectIndex(std::string objectName)
	{
		int i=-1;
		int n=sizeof(objectNames)/sizeof(objectNames[0]);
		int j=0;
		while(j<n)
		{
			if(objectNames[j]==objectName)
			{
				i=j;
				break;
			}
			j++;
		}
		return i;
	}

	bool objectOfInterest(std::vector<std::string> enabledObjectList, std::string objectName)
	{
		return (
			std::find(
				enabledObjectList.begin(), 
				enabledObjectList.end(), 
				objectName) != enabledObjectList.end()
			);
	}
	
} // namespace sample
} // namespace analytics
} // namespace vms_server_plugins
} // namespace nx
