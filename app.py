import sys

from controllers.Controller import Controller
from models.Model import Model
from views.View import View

if __name__ == '__main__':
    try:
        model = Model() # Loo mudel
        view = View(model) # Loo view andes kaasa model
        Controller(model, view) # Loo Controller
        view.mainloop() # Viimane rida koodis
    except FileNotFoundError as error:
        #print(f'Viga: {error}')
        View.show_message(error)
        sys.exit(1)
    except ValueError as error:
        View.show_message(error)
        sys.exit(1)
    except Exception as error:
        #print(f'tekkis ootamatu viga: {error}')
        View.show_message(error)
        sys.exit(1)