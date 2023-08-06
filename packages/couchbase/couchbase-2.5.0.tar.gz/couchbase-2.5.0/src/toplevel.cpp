//
// Created by Ellis Breen on 09/09/2018.
//

#include <map>
#include <string>
#include "toplevel.h"

typedef std::map<std::string,std::string> StringMap;
class stuff
{
    StringMap test;
};

#include "toplevel.h"


const char *pycbc_extract_from_map(void *my_map, const char *key) {
    StringMap* map=(StringMap *)(my_map);
    StringMap::const_iterator iterMap = map->find(key);
    return iterMap!=map->end()?iterMap->second.c_str():NULL;
}

void* pycbc_create_map(){
    return new StringMap();
}