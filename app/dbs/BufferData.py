class MySQLBufferData(object):
    def __init__(self):
        self._hot_key_tag_buffer = None
        self._user_key_tag_buffer = None
        self._data_collection_flag = False

    def have_buffer(self):
        return self._hot_key_tag_buffer is not None \
               and self._user_key_tag_buffer is not None

    def set_hot_key_tag_buffer(self, hot_key_tag_buffer):
        self._hot_key_tag_buffer = hot_key_tag_buffer

    def set_user_key_tag_buffer(self, user_key_tag_buffer):
        self._user_key_tag_buffer = user_key_tag_buffer

    def set_data_collection_flag(self, flag):
        self._data_collection_flag = flag

    def get_hot_key_tag_buffer(self, key):
        # print("get_hot_key_tag_buffer: {}".format(key))
        # print("get_hot_key_tag_buffer: {}".format(self._hot_key_tag_buffer.get(key, "")))
        return self._hot_key_tag_buffer.get(key, "")

    def get_user_key_tag_buffer(self, key):
        return self._user_key_tag_buffer.get(key, "")

    def get_data_collection_flag(self):
        return self._data_collection_flag
