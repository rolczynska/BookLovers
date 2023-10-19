from booklovers import forms

search = forms.Search("Zmierzch", "Rafał Rolczyński", ["Wolności", "Marcinkowskiego"],
                      "olkiewicz.alex@gmail.com")
search.send_register_confirmation()
