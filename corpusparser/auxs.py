def filename_from_key(key, data_folder = "data", ext = ".wav"):
    """ Takes the key, returns the filename """
    return data_folder + key + ext #TODO: consider improving this using os.path