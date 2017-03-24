from conceptnet5.util import get_support_data_filename
from conceptnet5.vectors import standardized_uri, get_vector, cosine_similarity, normalize_vec
from conceptnet5.vectors.transforms import l2_normalize_rows
import numpy as np
import pandas as pd


# A list of English words referring to nationalities, nations, ethnicities, and
# religions. Our goal is to prevent ConceptNet from learning insults and
# stereotypes about these classes of people.

PEOPLE_BY_CULTURE = [
    # Regions of the world
    'africa', 'african', 'sub-saharan',
    'america', 'american',
    'caribbean',
    'polynesia', 'polynesian',
    'asia', 'asian',
    'europe', 'european',
    'middle east', 'middle eastern',
    'arabia', 'arabian', 'arab'
    'latin america', 'latin american', 'latino', 'latina', 'hispanic',

    # Religions and beliefs
    'christianity', 'christian',
    'islam', 'muslim',
    'humanism', 'humanist', 'secular',
    'agnosticism', 'agnostic',
    'atheism', 'atheist',
    'buddhism', 'buddhist',
    'sikhism', 'sikh',
    'judaism', 'jewish',
    "bahà'i",
    'jainism', 'jain',
    'shinto',
    'zoroastrianism', 'zoroastrian',
    'paganism', 'pagan',

    # Colors used as races
    'white', 'black', 'brown',

    # A perhaps unnecessarily thorough list of countries (by Wikipedia's
    # definition, mostly).
    'abkhazia', 'abkhazian',
    'afghanistan', 'afghani',
    'albania', 'albanian',
    'algeria', 'algerian',
    'american samoa', 'american samoan',
    'andorra', 'andorran',
    'angola', 'angolan',
    'anguilla', 'anguillan',
    'antigua', 'antiguan', 'barbuda', 'barbudan',
    'argentina', 'argentinian',
    'armenia', 'armenian',
    'aruba', 'aruban',
    'australia', 'australian',
    'austria', 'austrian',
    'azerbaijan', 'azerbaijani',
    'bahamas', 'bahamian',
    'bahrain', 'bahraini',
    'bangladesh', 'bangladeshi',
    'barbados', 'barbadian',
    'belgium', 'belgian',
    'belarus', 'belarusian',
    'belize', 'belizean',
    'benin', 'beninese',
    'bermuda', 'bermudan',
    'bhutan', 'bhutanian',
    'bolivia', 'bolivian',
    'bonaire',
    'bosnia', 'bosnian', 'herzegovina', 'herzegovinian',
    'botswana', 'botswanan',
    'brazil', 'brazilian',
    'brunei', 'bruneian',
    'bulgaria', 'bulgarian',
    'burkina faso', 'burkinabé',
    'burma', 'burmese', 'myanmar',
    'burundi', 'burundian',
    'cabo verde', 'cape verde',
    'cambodia', 'cambodian',
    'cameroon', 'cameroonian',
    'canada', 'canadian',
    'cayman islands', 'caymanian',
    'central african republic',
    'chad', 'chadian',
    'chile', 'chilean',
    'china', 'chinese',
    'taiwan', 'taiwanese',
    'colombia', 'colombian',
    'comoros', 'comorian',
    'congo', 'congolese',
    'costa rica', 'costa rican',
    "côte d'ivoire", 'ivory coast', 'ivorian',
    'croatia', 'croatian',
    'cuba', 'cuban',
    'curaçao', 'curaçaoan',
    'cyprus', 'cypriot',
    'czech republic', 'czech', 'czechia',
    'denmark', 'danish',
    'djibouti', 'djiboutian',
    'dominica', 'dominican',
    'dominican republic',
    'east timor', 'timorese', 'timor-leste',
    'ecuador', 'ecuadoran',
    'egypt', 'egyptian',
    'el salvador', 'salvadoran',
    'england', 'english',
    'equatorial guinea', 'equatoguinean',
    'eritrea', 'eritrean',
    'estonia', 'estonian',
    'ethiopia', 'ethiopian',
    'faroe islands', 'faroese',
    'fiji', 'fijian',
    'finland', 'finnish',
    'france', 'french',
    'gabon', 'gabonese',
    'georgia', 'georgian',
    'germany', 'german',
    'ghana', 'ghanaian',
    'gibraltar',
    'great britain', 'british',
    'greece', 'greek',
    'greenland', 'greenlandic',
    'grenada', 'grenadian',
    'gambia', 'gambian',
    'guinea', 'guinean',
    'guatemala', 'guatemalan',
    'guadeloupe',
    'guam', 'guamanian',
    'guinea-bissau', 'bissau-guinean',
    'guyana', 'guyanese',
    'haiti', 'haitian',
    'honduras', 'honduran',
    'hong kong', 'hongkongese',
    'hungary', 'hungarian',
    'iceland', 'icelandic',
    'india', 'indian',
    'indonesia', 'indonesian',
    'iraq', 'iraqi',
    'iran', 'iranian',
    'ireland', 'irish',
    'isle of man', 'manx',
    'israel', 'israeli',
    'italy', 'italian',
    'jamaica', 'jamaican',
    'japan', 'japanese',
    'jordan', 'jordanian',
    'kazakhstan', 'kazakh',
    'kenya', 'kenyan',
    'kiribati', 'i-kiribati',
    'korea', 'korean',
    'north korea', 'north korean',
    'south korea', 'south korean',
    'kosovo', 'kosovar',
    'kuwait', 'kuwaiti',
    'kyrgyzstan', 'kyrgyz',
    'laos', 'laotian',
    'latvia', 'latvian',
    'lebanon', 'lebanese',
    'lesotho', 'basotho',
    'liberia', 'liberian',
    'libya', 'libyan',
    'liechtenstein', 'liechtensteiner',
    'lithuania', 'lithuanian',
    'luxembourg', 'luxembourgish',
    'macau', 'macanese',
    'macedonia', 'macedonian',
    'madagascar', 'malagasy',
    'malawi', 'malawian',
    'malaysia', 'malaysian',
    'maldives', 'maldivian',
    'mali', 'malinese',
    'malta', 'maltese',
    'marshall islands', 'marshallese',
    'martinique', 'martinican',
    'mauritania', 'mauritanian',
    'mauritius', 'mauritian',
    'mayotte', 'mahoran',
    'mexico', 'mexican',
    'micronesia', 'micronesian',
    'moldova', 'moldovan',
    'monaco', 'monégasque',
    'mongolia', 'mongolian',
    'montenegro', 'montenegrin',
    'morocco', 'moroccan',
    'mozambique', 'mozambican',
    'namibia', 'namibian',
    'nauru', 'nauruan',
    'nepal', 'nepali',
    'netherlands', 'dutch',
    'new caledonia', 'new caledonian',
    'new zealand',
    'nicaragua', 'nicaraguan',
    'niger', 'nigerien',
    'nigeria', 'nigerian',
    'niue', 'niuean',
    'norway', 'norwegian',
    'oman', 'omani',
    'pakistan', 'pakistani',
    'palau', 'palauan',
    'palestine', 'palestinian',
    'panama', 'panamanian',
    'papua new guinea', 'papuan',
    'paraguay', 'paraguayan',
    'peru', 'peruvian',
    'phillipines', 'filipino',
    'poland',
    'portugal', 'portuguese',
    'puerto rico', 'puerto rican',
    'qatar', 'qatari',
    'réunion', 'réunionese',
    'romania', 'romanian',
    'russia', 'russian',
    'rwanda', 'rwandan',
    'saint lucia', 'saint lucian',
    'saint vincent and the grenadines', 'vincentian',
    'samoa', 'samoan',
    'san marino', 'sammarinese',
    'são tome and principe', 'são toméan',
    'saudi arabia', 'saudi arabian',
    'scotland', 'scottish',
    'senegal', 'senegalese',
    'serbia', 'serbian',
    'seychelles', 'seychellois',
    'sierra leone', 'sierra leonean',
    'singapore', 'singaporean',
    'slovakia', 'slovakian',
    'slovenia', 'slovenian',
    'somalia', 'somalian',
    'somaliland', 'somalilander',
    'south africa', 'south african',
    'south sudan', 'south sudanese',
    'spain', 'spanish',
    'sri lanka', 'sri lankan',
    'sudan', 'sudanese',
    'surinam', 'surinamese',
    'svalbard',
    'swaziland', 'swazi',
    'sweden', 'swedish',
    'switzerland', 'swiss',
    'syria', 'syrian',
    'tajikistan', 'tajikistani',
    'tanzania', 'tanzanian',
    'thailand', 'thai',
    'togo', 'togolese',
    'tokelau', 'tokelauan',
    'tonga', 'tongan',
    'trinidad', 'trinidadian',
    'tobago', 'tobagonian',
    'tunisia', 'tunisian',
    'turkey', 'turkish',
    'turkmenistan', 'turkmen',
    'tuvalu', 'tuvaluan',
    'uganda', 'ugandan',
    'ukraine', 'ukrainian',
    'united arab emirates', 'emirati',
    'united kingdom',
    'united states',
    'uruguay', 'uruguayan',
    'uzbekistan', 'uzbek',
    'vanuatu', 'vanuatuan',
    'venezuela', 'venezuelan',
    'vietnam', 'vietnamese',
    'virgin islands',
    'wales', 'welsh',
    'wallis and futuna', 'wallisian', 'futunan',
    'western sahara', 'sahrawi',
    'yemen', 'yemeni',
    'zambia', 'zambian',
    'zimbabwe', 'zimbabwean'
]

# A list of things we don't want our semantic space to learn about various
# cultures of people. This list doesn't have to be exhaustive; we're modifying
# the whole vector space, so nearby terms will also be affected.
CULTURE_PREJUDICES = [
    'illegal', 'terror', 'evil', 'threat',
    'dumbass', 'shithead', 'wanker',
    'illiterate', 'ignorant', 'inferior',
    'sexy', 'suave',
    'wealthy', 'poor',
    'racist', 'slavery',
    'torture', 'fascist', 'persecute',
    'fraudster', 'rapist', 'robber', 'dodgy', 'perpetrator',
]

# Because it combines information from different sources, Numberbatch seems to
# automatically counteract the worst gender biases of word2vec, particularly
# those that assign genders to professions.
#
# However, Numberbatch acquires a "porn bias" from the Common Crawl via GloVe.
# Because so much of the Web is about porn, words such as 'teen', 'girl', and
# 'girlfriend' acquire word associations from porn.
#
# We handle this and related problems by making an axis of words that refer to
# gender or sexual orientation, and exclude them from making associations with
# porn and sexually-degrading words. It appears we don't have to handle the
# word 'teen' separately; it's fixed as a side effect when we de-porn the more
# specifically gendered words.

FEMALE_WORDS = [
    'woman', 'feminine', 'female',
    'girl', 'girlfriend', 'wife', 'mother', 'sister', 'daughter',
]

MALE_WORDS = [
    'man', 'masculine', 'male',
    'boy', 'boyfriend', 'husband', 'father', 'brother', 'son'
]

ORIENTATION_WORDS = [
    'gay', 'lesbian', 'bisexual', 'trans', 'transgender'
]

SEX_PREJUDICES = [
    'slut', 'whore', 'shrew', 'bitch', 'faggot',
    'sexy', 'fuck', 'fucked', 'fucker', 'nude', 'porn'
]


def read_sentiment(filename):
    sentiments = {}
    for line in open(filename, encoding='utf-8'):
        line = line.strip()
        if line and not line.startswith('#'):
            word, sentiment_str = line.split(',')
            sentiments[word] = float(sentiment_str)
    return sentiments


def get_weighted_vector(frame, weighted_terms):
    total = frame.iloc[0] * 0.
    for term, weight in weighted_terms:
        if term in frame.index:
            vec = frame.loc[term]
            total += vec * weight
    return normalize_vec(total)


def get_category_axis(frame, category_examples):
    return get_weighted_vector(
        frame,
        [(standardized_uri('en', term), 1.)
         for term in category_examples]
    )


def reject_subspace(frame, axes):
    current_array = frame.copy()
    for axis in axes:
        axis = normalize_vec(axis)
        projection = current_array.dot(axis)
        current_array -= np.outer(projection, axis)

    return l2_normalize_rows(current_array, offset=1e-9)


def de_bias_category(frame, category_examples, bias_examples, strength=20.):
    category_axis = get_category_axis(frame, category_examples)

    applicability = frame.dot(category_axis)
    applicability = np.power(np.maximum(applicability, 0.), 1 / strength)

    vocab = [
        standardized_uri('en', term) for term in bias_examples
    ]
    components_to_reject = frame.loc[vocab].values
    modified_component = reject_subspace(frame, components_to_reject).mul(applicability, axis=0)
    original_component = frame.mul(1 - applicability, axis=0)
    return l2_normalize_rows(original_component + modified_component)


def de_bias_frame(frame):
    """
    Take in a DataFrame representing a semantic space, and make a strong
    effort to modify it to remove biases and prejudices against certain
    classes of people.

    The resulting space attempts not to learn stereotyped associations with
    anyone's race, color, religion, national origin, sex, gender presentation,
    or sexual orientation.
    """
    newframe = de_bias_category(frame, PEOPLE_BY_CULTURE, CULTURE_PREJUDICES)
    newframe = de_bias_category(newframe, FEMALE_WORDS + MALE_WORDS + ORIENTATION_WORDS, SEX_PREJUDICES)
    return newframe
