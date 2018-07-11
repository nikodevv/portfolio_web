import { createStore } from 'redux';
import heroSearchApp from './reducers.js';
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