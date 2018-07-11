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


/**Other constants */
const SRCH_RELEVANCE_STATES = {
    REL: 'SEARCH_RELEVANT',
    DISQ: "SEARCH_DISQUALIFIED"
};

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

// Reducers (specify how state will change)

const initialState = {
    relevance: SRCH_RELEVANCE_STATES.REL,
    SEARCH_STR: ""
};

function heroSearchApp(state = initialState, action){
    switch (action.type){
        case S_REL:
            return Object.assign({},state, 
                {relevance: SRCH_RELEVANCE_STATES.REL});
        case S_DISQ:
            return Object.assign({}, state, 
                {relevance: SRCH_RELEVANCE_STATES.DISQ});
        case ADD_TO_HERO_SRCH:
            return Object.assign({}, state, {SEARCH_STR: state.SEARCH_STR + action.key});
        
        case RMV_FRM_HERO_SRCH:
            if (state.SEARCH_STR===""){
                return Object.assign({},state);
            }
            else{
                const STR = state.SEARC_STR;
                return Object.assign({}, state, 
                    {SEARCH_STR: STR.substring(0,STR.length-1)});
            }
        case ADD_TO_HERO_SRCH:
            return Object.assign({}, state, {SEARCH_STR: ""});

        default:
            return state;
    };
}
