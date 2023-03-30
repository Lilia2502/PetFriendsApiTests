from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

#Test 1
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result
    print(f'\n {email}, {password}, {status}, {result}')

#Test 2
def test_get_api_key_with_correct_mail_and_wrong_passwor(email=valid_email, password=invalid_password):
    """Проверяем запрос с правильным email и c неправильным паролем."""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным паролем')

#Test 3
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    """Проверяем запрос с неправильным email и с правильным паролем."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email')

#Test 4
def test_get_api_key_with_wrong_email_and_wrong_password(email=invalid_email, password=invalid_password):
    """Проверяем запрос с неправильным email и с неправильным паролем."""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email и паролем')

#Test 5
def test_get_all_pets_with_valid_key(filter='my_pets'):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    num = len(result['pets'])
    if filter == 'my_pets':
        print(f'{num} my pets на сайте')
    else:
        print(f'список не пустой')

#Test 6
def test_add_new_pet_with_valid_data(name='Alisa', animal_type='белая', age='3', pet_photo='images/cat15.jpg'):
    """Проверяем,  добавление питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')

#Test 7
def test_add_new_pet_with_invalid_foto(name='Барсик', animal_type='Серый', age='1', pet_photo='images/cat2.jpg'):
    """Проверяем,  добавление питомца с некорректным именем фойла с фото."""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    if not os.path.exists(pet_photo):
        print(f'\n нет {pet_photo}')
        pet_photo = 'images/dd5.jpg'
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        print(f'Замена на аватар на {pet_photo}')

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')

#Test 8
def test_add_pet_with_a_lot_of_age_in_variable_age(name='Бакс', animal_type='Пушистый', pet_photo='images/c17.jpg'):
    """Добавления очень взрослого питомца с большим возрастом."""
    age = '1000'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = float(result['age'])
    assert status == 200
    assert (age > 20 or age < 0), 'Добавлен питомец с невозможным возрастом, меньше 0 или старше 20 лет.'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом, меньше 0 или старше 20 лет. {age}')

#Test 9
def test_add_pet_with_variable_age_symble(name='Мурка', animal_type='Белая', pet_photo='images/cat10.jpg'):
    """Добавления питомца с символами в поле возраста."""
    age = '@%#'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert age, 'Добавлен питомец с невозможным возрастом'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом {age}')

#Test 10
def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='Кот', age='2', pet_photo='images/d3.jpg'):
    """ Добавления питомца с именем, которое превышает 10 слов."""

    name = 'у лукоморья дуб зеленый златая цепь на дубе том и днем и ночью кот ученый все бродит по цепи кругом'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count > 10, 'Питомец добавлен с именем больше 10 слов'
    print('ok')
    print(f'Сайт позволяет добавлять  питомецев с именем больше 10 слов. {word_count}')

#Test 11
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Рыжик", "кот", "2", "images/c12.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')

#Test 12
def test_successful_update_self_pet_info(name='Вискас', animal_type='Белый', age=3):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
        print('ok')
        print(result)
    else:
        raise Exception("This is not my pet")

#Test 13
def test_add_pet_with_a_lot_of_symbol_in_variable_name(animal_type='Кот', age='0', pet_photo='images/c3.jpg'):
    """Добавления питомца с именем, которое имеет слишком длинное значение"""

    name = 'qwertyuiopoiuytrewqwertyuiopoiutr'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_name = result['name']
    symbol_count = len(list_name)

    assert status == 200
    assert symbol_count > 30, 'Питомец добавлен с именем больше 30 символов.'
    print(f'\n Добавлен питомец с именем больше 30 символов. {symbol_count}')


#Test 14
def test_add_pet_with_special_characters_in_variable_animal_type(name='Мороз', age='1', pet_photo='images/c5.jpg'):
    """ Добавление питомца с использованием специальных символов вместо букв в переменной animal_type.."""

    animal_type = '.%?(№'
    symbols = '"7#@8*$'
    symbol = []

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    for i in symbols:
        if i in result['animal_type']:
            symbol.append(i)
    assert symbol[0] in result['animal_type'], 'Питомец добавлен с недопустимыми специальными символами.'
    print(f'\n Добавлен питомец с недопустимыми специальными символами. {symbols}')

# est 15
def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Алекс', age='5', pet_photo='images/c7.jpg'):
    """Проверка с негативным сценарием.
    Добавления питомца с полем "Породы", которое свыше 10 слов."""

    animal_type = 'у лукоморья дуб зеленый златая цепь на дубе том и днем и ночью кот ученый все ходит по цепи кругом'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type'].split()
    word_count = len(list_animal_type)

    assert status == 200
    assert word_count > 10, 'Питомец добавлен в приложение с названием породы больше 10 слов.'
    print(f'\n Добавлен питомец с названием породы больше 10 слов. {word_count}')

#Test 16
def test_add_pet_with_a_lot_of_symbol_in_variable_animal_type(name='Барсик', age='1', pet_photo='images/cat2.jpg'):
    """Добавления питомца с полем "Порода", которое имеет слишком длинное значение.
    Сообщение, если питомец будет добавлен в приложение с названием породы состоящим из 55 символов."""

    animal_type = 'qwertyuiopoiuytrewqwertyuiopoiuytrewqwertyuiopoiuytrewq'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    list_animal_type = result['animal_type']
    symbol_count = len(list_animal_type)

    assert status == 200
    assert symbol_count > 25, 'Питомец добавлен в приложение с названием породы более чем из 25 символов.'
    print(f'\n Добавлен питомец с названием породы породы более чем из 25 символов. {symbol_count}')

