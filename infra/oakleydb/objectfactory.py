class ObjectFactory(object):

    # creates an empty lens details dictionary to allow us to always have the correct fields
    @staticmethod
    def create_lens_details(lens):
        details = {'name': '', 'base': '', 'coating': '', 'transmission': '', 'transindex': 0,
                   'purpose': '', 'lighting': '', 'lenstype': '', 'url': '', 'typeid': -1}

        if 'name' in lens:
            details['name'] = lens['name']

        if 'lenstype' in lens:
            details['lenstype'] = lens['lenstype']

        if 'url' in lens:
            details['url'] = lens['url']

        return details
