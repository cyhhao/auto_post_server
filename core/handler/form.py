# coding=utf-8
class Option(object):
    def __init__(self, type, default, order, title=''):
        self.title = title
        self.default = default
        self.type = type
        self.group = []
        self.order = order

    def append_item(self, key, title, href=None):
        item = {
            "key": key,
            "title": title
        }
        if href:
            item["href"] = href
        self.group.append(item)

    def render(self):
        data = {
            "type": self.type,
            "ans": self.default
        }
        if self.order:
            data['order'] = self.order
        if self.group and len(self.group) > 0:
            data['group'] = self.group

        return data


class CheckBox(Option):
    def __init__(self, default=None, order='|', title='', ):
        if default is None:
            default = []
        super(CheckBox, self).__init__("checkbox", default, order, title)


class Radio(Option):
    def __init__(self, default='', order='-', title=''):
        super(Radio, self).__init__("radio", default, order, title)


class Input(Option):
    def __init__(self, title='', default='', type='input'):
        super(Input, self).__init__(type, default, None, title)


class Form:
    CheckBox = CheckBox
    Radio = Radio
    Input = Input

    def __init__(self, title, button, description):
        self.init(title, button, description)

    def init(self, title, button, description):
        self.title = title
        self.button = button
        self.description = description
        self.extra = []

    def append_extra(self, option):
        self.extra.append(option)

    def render(self):
        data = {
            "title": self.title,
            "button": self.button,
        }
        description = {
            "content": self.description
        }
        if len(self.extra) > 0:
            extra_list = []
            for ex in self.extra:
                extra_list.append(ex.render())
            description['extra'] = extra_list

        data['description'] = description

        return data
