# Copyright (C) 2022 Im Yongsik


def ImportFile(filepath):
    f = open(filepath, "r")
    contents = f.read()
    print(contents)
    f.close()
    return {"FINISHED"}
