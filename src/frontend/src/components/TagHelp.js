import React from 'react'
import {
  List,
  ListItem,
  ListItemText,
  Typography,
  Divider
} from '@material-ui/core';


// TODO: use BE endpoint to retrive info about tags
const info = [
    {
        'title': 'CC: conjunction, coordinating',
        'help': `& 'n and both but either et for less minus neither nor
                or plus so therefore times v. versus vs. whether yet`
    },
    {
        'title': 'CD: numeral, cardinal',
        'help': `mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-
seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025
fifteen 271,124 dozen quintillion DM2,000 ...`
    },
    {
        'title': 'DT: determiner',
        'help': `all an another any both del each either every half la many much nary
neither no some such that the them these this those`
    },
    {
        'title': 'EX: existential there',
        'help': `there`
    },
    {
        'title': 'IN: preposition or conjunction, subordinating',
        'help': `astride among uppon whether out inside pro despite on by throughout
below within for towards near behind atop around if like until below
next into if beside ...`
    },
    {
        'title': 'JJ: adjective or numeral, ordinal',
        'help': `third ill-mannered pre-war regrettable oiled calamitous first separable
ectoplasmic battery-powered participatory fourth still-to-be-named
multilingual multi-disciplinary ...`
    },
    {
        'title': 'JJR: adjective, comparative',
        'help': `bleaker braver breezier briefer brighter brisker broader bumper busier
calmer cheaper choosier cleaner clearer closer colder commoner costlier
cozier creamier crunchier cuter ...`
    },
    {
        'title': 'JJS: adjective, superlative',
        'help': `calmest cheapest choicest classiest cleanest clearest closest commonest
corniest costliest crassest creepiest crudest cutest darkest deadliest
dearest deepest densest dinkiest ...`
    },
    {
        'title': 'LS: list item marker',
        'help': `A A. B B. C C. D E F First G H I J K One SP-44001 SP-44002 SP-44005
SP-44007 Second Third Three Two * a b c d first five four one six three
two`
    },
    {
        'title': 'CC: conjunction, coordinating',
        'help': `& 'n and both but either et for less minus neither nor
                or plus so therefore times v. versus vs. whether yet`
    },
    {
        'title': 'MD: modal auxiliary',
        'help': `can cannot could couldn't dare may might must need ought shall should
shouldn't will would`
    },
    {
        'title': 'NN: noun, common, singular or mass',
        'help': `common-carrier cabbage knuckle-duster Casino afghan shed thermostat
investment slide humour falloff slick wind hyena override subhumanity
machinist ...`
    },
    {
        'title': 'NNP: noun, proper, singular',
        'help': `Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos
Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA
Shannon A.K.C. Meltex Liverpool ...`
    },
    {
        'title': 'NNS: noun, common, plural',
        'help': `undergraduates scotches bric-a-brac products bodyguards facets coasts
divestitures storehouses designs clubs fragrances averages
subjectivists apprehensions muses factory-jobs ...`
    },
    {
        'title': 'PDT: pre-determiner',
        'help': `all both half many quite such sure this`
    },
    {
        'title': 'POS: genitive marker',
        'help': `' 's`
    },
    {
        'title': 'PRP: pronoun, personal',
        'help': `hers herself him himself hisself it itself me myself one oneself ours
ourselves ownself self she thee theirs them themselves they thou thy us`
    },
    {
        'title': 'PRP$: pronoun, possessive',
        'help': `her his mine my our ours their thy your`
    },
    {
        'title': 'RB: adverb',
        'help': `occasionally unabatingly maddeningly adventurously professedly
stirringly prominently technologically magisterially predominately
swiftly fiscally pitilessly ...`
    },
    {
        'title': 'RBR: adverb, comparative',
        'help': `further gloomier grander graver greater grimmer harder harsher
healthier heavier higher however larger later leaner lengthier less-
perfectly lesser lonelier longer louder lower more ...`
    },
    {
        'title': 'RBS: adverb, superlative',
        'help': `best biggest bluntest earliest farthest first furthest hardest
heartiest highest largest least less most nearest second tightest worst`
    },
    {
        'title': 'RP: particle',
        'help': `aboard about across along apart around aside at away back before behind
by crop down ever fast for forth from go high i.e. in into just later
low more off on open out over per pie raising start teeth that through
under unto up up-pp upon whole with you`
    },
    {
        'title': 'TO: "to" as preposition or infinitive marker',
        'help': `to`
    },
    {
        'title': 'UH: interjection',
        'help': `Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen
huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly
man baby diddle hush sonuvabitch ...`
    },
    {
        'title': 'VB: verb, base form',
        'help': `ask assemble assess assign assume atone attention avoid bake balkanize
bank begin behold believe bend benefit bevel beware bless boil bomb
boost brace break bring broil brush build ...`
    },
    {
        'title': 'VBD: verb, past tense',
        'help': `dipped pleaded swiped regummed soaked tidied convened halted registered
cushioned exacted snubbed strode aimed adopted belied figgered
speculated wore appreciated contemplated ...`
    },
    {
        'title': 'VBG: verb, present participle or gerund',
        'help': `telegraphing stirring focusing angering judging stalling lactating
hankerin' alleging veering capping approaching traveling besieging
encrypting interrupting erasing wincing ...`
    },
    {
        'title': 'VBN: verb, past participle',
        'help': `multihulled dilapidated aerosolized chaired languished panelized used
experimented flourished imitated reunifed factored condensed sheared
unsettled primed dubbed desired ...`
    },
    {
        'title': 'VBP: verb, present tense, not 3rd person singular',
        'help': `predominate wrap resort sue twist spill cure lengthen brush terminate
appear tend stray glisten obtain comprise detest tease attract
emphasize mold postpone sever return wag ...`
    },
    {
        'title': 'VBZ: verb, present tense, 3rd person singular',
        'help': `bases reconstructs marks mixes displeases seals carps weaves snatches
slumps stretches authorizes smolders pictures emerges stockpiles
seduces fizzes uses bolsters slaps speaks pleads ...`
    },
    {
        'title': 'WDT: WH-determiner',
        'help': `that what whatever which whichever`
    },
    {
        'title': 'WP: WH-pronoun',
        'help': `that what whatever whatsoever which who whom whosoever`
    },
    {
        'title': 'WRB: Wh-adverb',
        'help': `how however whence whenever where whereby whereever wherein whereof why`
    },
]


export default class TagHelp extends React.Component {
    render() {
         return (
              <List>
                  {info.map((item) =>
                   <div>
                   <ListItem>
                       <ListItemText
                         primary=<Typography gutterBottom variant="h4">{item.title}</Typography>
                         secondary={item.help}
                       />
                   </ListItem>
                   <Divider />
                   </div>
                )}
              </List>
         );
    }
}
