class ObjectFactory(object):

    # creates an empty lens details dictionary to allow us to always have the correct fields
    @staticmethod
    def create_lens_details(lens):
        details = {'id': -1, 'name': '', 'base': '', 'coating': '', 'transmission': '', 'transindex': 0,
                   'purpose': '', 'lighting': '', 'lenstype': '', 'url': '', 'typeid': -1}

        if 'name' in lens:
            details['name'] = lens['name']

        if 'lenstype' in lens:
            details['lenstype'] = lens['lenstype']

        if 'url' in lens:
            details['url'] = lens['url']

        if 'typeid' in lens:
            details['typeid'] = lens['typeid']

        return details

    @staticmethod
    def create_style(style):
        ret_style = {'id': -1, 'name': '', 'url': '', 'family': ''}

        if 'name' in style:
            ret_style['name'] = style['name']

        if 'url' in style:
            ret_style['url'] = style['url']

        if 'family' in style:
            ret_style['family'] = style['family']

        return ret_style

    @staticmethod
    def create_model_details(model):
        details = {'id': -1, 'name': '', 'style': '', 'sku': '', 'listprice': '', 'url': '', 'frame': '',
                   'lens': '', 'fit': ''}

        if 'id' in model:
            details['id'] = model['id']

        if 'name' in model:
            details['name'] = model['name']

        if 'style' in model:
            details['style'] = model['style']

        if 'sku' in model:
            details['sku'] = model['sku']

        if 'listprice' in model:
            details['listprice'] = model['listprice']

        if 'url' in model:
            details['url'] = model['url']

        if 'frame' in model:
            details['frame'] = model['frame']

        if 'lens' in model:
            details['lens'] = model['lens']

        if 'fit' in model:
            details['fit'] = model['fit']

        return details
