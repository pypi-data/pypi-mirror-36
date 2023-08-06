//
// Created by Ellis Breen on 09/09/2018.
//

#ifndef COUCHBASE_PYTHON_CLIENT_2_3_1_TOPLEVEL1_H
#define COUCHBASE_PYTHON_CLIENT_2_3_1_TOPLEVEL1_H

extern const char* pycbc_extract_from_map(void *my_map, const char *key);
#ifdef __cplusplus
extern "C"{
#endif
    void* pycbc_create_map();
#ifdef __cplusplus
}
#endif

#endif //COUCHBASE_PYTHON_CLIENT_2_3_1_TOPLEVEL1_H
