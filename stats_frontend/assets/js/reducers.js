"use strict";

/** Actions */
// 'type' for non-search relevant heros
const S_DISQ = 'SET_DISQUALIFIED';
// 'type' for search-relevant heroes
const S_REL = 'SET_RELEVANT';
// add text to hero filter string
const ADD_TO_HERO_SRCH = "ADD_TO_SEARCH_STR";
// remove text from filter string
const RMV_FRM_HERO_SRCH = "REMOVE_FROM_SEARCH_STR";
// delete filter string
const DEL_HERO_SRCH = "DELETE_HERO_SEARCH_STR";


/**Action Creators */
// why the fuck do i need these
function offToggleRelevantHero(heroID){
    return {
        type: S_DISQ,
        heroID: heroID
    };
};
function onToggleRelevantHero(heroID){
    return{
        type: S_REL,
        heroID: heroID
    }
};
function extendHeroSearchStr(key){
    return{
        type: ADD_TO_HERO_SRCH,
        key: key
    };
};
function reduceHeroSearchStr(){
    return{type: RMV_FRM_HERO_SRCH};
};
function deleteHeroSearchStr(){
    return{type: DEL_HERO_SRCH};
};

var generateHeroCards = function(){
    var heroCards = Array(115);
    for (i=0;i<heroCards.length-1;i++){
        heroCards[i] = { 
            heroID = heroCards[i],
            searchRelevant = true,
        }
    };
    return heroCards;
};

var initialState = {
    heroCards: generateHeroCards(),
    searchStr: ""
};


// Reducers (specify how state will change)
function heroCardFilter(state =[], action){
    switch(action.type){
        // sets a given heroCards as search relevant
        case S_REL:
            var heroCards = state;
            heroCards[action.heroID-1].searchRelevant = true;
            return heroCards;
        case S_DISQ:
            var heroCards = state;
            heroCards[action.heroID-1].searchRelevant = false;
            return heroCards;
        };
};

function srchFilterUpdate(state="", action){
    switch(action.type){
        case ADD_TO_HERO_SRCH:
            return state + action.key
        case RMV_FRM_HERO_SRCH:
            if(state===""){
                return state
            }
            else{
                state.substring(0,state.length-1)
            };
        case DEL_HERO_SRCH:
            return "";
    };
};

function heroSearchApp(state = initialState, action){
    switch (action.type){
        case S_REL:
            return Object.assign({}, state, {heroCards: heroCardFilter(state.heroCards, action)})
        case S_DISQ:
            return Object.assign({}, state, {heroCards: heroCardFilter(state.heroCards, action)})

        case ADD_TO_HERO_SRCH:
            return Object.assign({}, state,
                {searchStr: srchFilterUpdate(state.searchStr, action)})
        
        case RMV_FRM_HERO_SRCH:
            return Object.assign({}, state, srchFilterUpdate(state.searchStr, action))

        case DEL_HERO_SRCH:
            return Object.assign({}, state, {searchStr: srchFilterUpdate(state.searchStr, action)});

        default:
            return state;
    };
};

export default heroSearchApp;