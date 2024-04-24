class PromptTemplate:
    def __init__(self, input_variables, template):
        self.input_variables = input_variables
        self.template = template
    
    def fill_template(self, **kwargs):
        filled_template = self.template.format(**kwargs)
        return filled_template