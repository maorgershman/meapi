from random import choice, uniform, randint
from re import sub

from meapi.exceptions import MeException

random_names = ['Kian Summers', 'Alissa James', 'Danny Schneider', 'Matteo Galloway', 'Mario Wells',
                'Mercedes Arellano',
                'Areli Matthews', 'Lana Good', 'Gina Berg', 'Leo Woods', 'Sabrina Herman', 'Livia Bell', 'Kara Knapp',
                'Rory Fitzgerald', 'Sandra Moreno', 'Ashley Shepard', 'Ashleigh Soto', 'Cornelius Glover',
                'Everett Chung',
                'Maxim Frye', 'Stephen Dyer', 'Adan Torres', 'Blaze Ortiz', 'Kellen Russo', 'Case Cole', 'Maia Barnes',
                'Dulce Nichols', 'Howard Decker', 'Cecelia Stuart', 'Arthur Jones', 'Isaias Jensen',
                'Alexander Russell',
                'Rex Deleon', 'Amirah Calderon', 'Julien Pollard', 'Kasey Adkins', 'Tess Sanford', 'Kallie Montes',
                'Keagan Sparks', 'Leticia Franklin', 'Jenna Newton', 'Rene Padilla', 'Nathalia Garza', 'Selena Sanford',
                'Francisco Kirby', 'Jonas Jacobson', 'Francis Khan', 'Ben Bush', 'Cyrus Suarez', 'Briana Pace',
                'Cory Coffey',
                'Lilian Heath', 'Matilda Ibarra', 'Laney Brown', 'Anna Baxter', 'Nathaly Kline', 'Arthur Humphrey',
                'Elianna Lin', 'Romeo Hull', 'Christina Page', 'Kristen Norris', 'Madison Holland', 'Deacon Heath',
                'Drew Nielsen', 'Skye Beck', 'Faith Chavez', 'Brenda Stuart', 'Davon Booth', 'Jayleen Logan',
                'Phoenix Hendricks', 'Ernesto Mcknight', 'Cael Jackson', 'Amari Mckinney', 'Mckinley Burke',
                'Chelsea Zamora',
                'Gillian Walker', 'Carleigh Zhang', 'Jewel Vaughn', 'Haven Foley', 'Itzel Benson', 'Emmy Conrad',
                'Salma Coleman', 'Alexzander Jensen', 'Raphael Morgan', 'Larissa Phillips', 'Simeon Boyle',
                'Maxwell Becker',
                'Janiyah Guerrero', 'Finley Mcmahon', 'Emily Montoya', 'Isis Logan', 'Rishi Pratt',
                'Alexzander Sanford',
                'Santos Stanley', 'Parker Wu', 'Jeffery Mercado', 'Giuliana Hoover', 'Maia Mcneil', 'Nehemiah Carson',
                'Victoria Weber', 'Zoe Foley', 'Nevaeh Jones', 'Naomi Mcneil', 'Janiya Wyatt', 'Laney Rowland',
                'Landyn Espinoza', 'Callum Hardin', 'Emerson Singleton']

random_phones = [
    '(660) 922-6553', '(580) 515-6505', '(688) 807-0149', '(263) 525-9876', '(410) 904-9366', '(371) 748-6602',
    '(504) 650-6138', '(386) 234-8057', '(995) 870-7237', '(204) 469-7256', '(446) 214-6917', '(573) 279-6423',
    '(757) 284-0184', '(425) 327-4356', '(282) 490-2711', '(498) 554-6862', '(267) 394-2873', '(250) 877-9300',
    '(365) 309-3605', '(653) 859-8552', '(295) 681-4985', '(917) 209-9126', '(259) 456-7261', '(636) 602-0051',
    '(546) 939-4709', '(696) 216-3191', '(942) 547-0438', '(617) 521-1063', '(834) 320-4697', '(289) 715-9002',
    '(287) 743-4787', '(233) 211-5477', '(310) 507-9518', '(668) 855-7965', '(462) 925-6287', '(225) 989-8122',
    '(446) 445-1273', '(495) 833-8519', '(749) 636-1076', '(390) 687-9989', '(620) 591-1072', '(206) 226-4777',
    '(445) 849-7978', '(306) 888-0088', '(304) 645-5223', '(842) 515-3114', '(745) 746-5739', '(787) 280-9669',
    '(214) 690-9671', '(799) 677-9893', '(757) 394-8573', '(247) 818-5774', '(464) 480-9306', '(633) 886-4550',
    '(785) 201-6640', '(232) 725-5171', '(890) 407-1692', '(823) 219-6096', '(694) 588-7717', '(571) 759-8546',
    '(349) 819-5109', '(663) 687-3045', '(640) 972-3875', '(817) 623-5718', '(946) 288-5778', '(397) 499-6533',
    '(200) 809-8563', '(561) 918-9344', '(757) 324-3738', '(951) 257-5699', '(592) 555-0273', '(414) 687-7908',
    '(990) 709-8256', '(310) 714-8860', '(795) 358-7649', '(216) 472-2217', '(790) 525-2678', '(823) 456-8232',
    '(802) 210-1298', '(271) 362-2554', '(301) 519-6081', '(957) 935-5358', '(545) 865-4100', '(746) 359-7511',
    '(400) 520-7528', '(283) 361-7508', '(575) 415-3752', '(474) 709-9438', '(614) 297-2741', '(699) 640-8816',
    '(760) 373-6541', '(969) 488-0062', '(575) 772-6734', '(818) 898-4142', '(475) 735-6936', '(209) 687-0867',
    '(481) 499-1650', '(240) 568-6034', '(895) 884-2492', '(284) 570-8356', '(733) 958-6883', '(905) 286-2798',
    '(910) 283-0866', '(968) 298-1232', '(713) 862-0522', '(736) 362-6571', '(251) 628-1422', '(258) 509-9633',
    '(716) 991-3793', '(999) 678-5578', '(894) 634-4534', '(735) 307-1144', '(951) 655-0566', '(631) 460-5947',
    '(238) 270-8264', '(617) 363-5309', '(744) 707-2887', '(475) 851-3555', '(699) 236-9982',
    '(480) 421-1021']

call_types = ['missed', 'outgoing', 'incoming']


def get_random_data(contacts=True, calls=True, location=True) -> dict:
    if not contacts and not calls and not location:
        raise MeException("You need to set True at least one of the random data types")

    random_data = {}

    if contacts:
        random_data['contacts'] = []
        for contact in range(1, randint(10, 30)):
            random_data['contacts'].append({
                "country_code": "XX",
                "date_of_birth": None,
                "name": str(choice(random_names)),
                "phone_number": int(sub(r'[\D]', '', str(choice(random_phones))))
            })
    if calls:
        random_data['calls'] = []
        for call in range(1, randint(10, 30)):
            random_data['calls'].append({
                "called_at": f"{randint(2018, 2022)}-{randint(1, 12)}-{randint(1, 31)}T{randint(1, 23)}:{randint(10, 59)}:{randint(10, 59)}Z",
                "duration": randint(10, 300),
                "name": str(choice(random_names)),
                "phone_number": int(sub(r'[\D]', '', str(choice(random_phones)))),
                "tag": None,
                "type": choice(call_types)
            })
    if location:
        random_data['location'] = {}
        random_data['location']['lat'] = - round(uniform(30, 60), 5)
        random_data['location']['lon'] = round(uniform(30, 60), 5)

    return random_data
