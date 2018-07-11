import {createStore} from 'redux';
import {heroSearchApp} from './reducers';
import {
    offToggleRelevantHero,
    onToggleRelevantHero,
    extendHeroSearchStr,
    reduceHeroSearchStr,
    deleteHeroSearchStr
} from './reducers';
const store = createStore(heroSearchApp);
//log initial state
console.log(store.getState())