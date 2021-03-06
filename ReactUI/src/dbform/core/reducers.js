import { combineReducers } from 'redux';
import { ADD_STRUCTURE, ADD_STRUCTURES, EDIT_STRUCTURE, DELETE_STRUCTURE, ADD_SETTINGS, ADD_FIELDS, ADD_USERS, ADD_PAGES } from './constants';
import { request, modal, magic, additives } from '../../base/reducers';

const defaultSettings = {
  tabs: {
    tabPosition: 'top',
    size: 'large',
  },
  grid: {
    xs: 1,
    sm: 2,
    md: 3,
    lg: 3,
    xl: 3,
    xxl: 4,
  },
  condition: {
    temperature: 298,
    pressure: 1,
  },
  auto_reset: false,
  full: 0,
};


export const structures = (state = [], action) => {
  switch (action.type) {
    case ADD_STRUCTURE:
      return state.map((data) => {
        if (data.record === action.record) {
          return {
            ...data,
            ...action.data,
          };
        }
        return data;
      });

    case ADD_STRUCTURES:
      return action.structures;

    case EDIT_STRUCTURE:
      return state.map(data =>
        (data.record === action.record ?
          action.data :
          data),
      );

    case DELETE_STRUCTURE:
      return state.filter(structure =>
        structure.record !== action.record,
      );

    default:
      return state;
  }
};

function getSettings() {
  const settigsOnStorageJson = localStorage.getItem('settings');
  if (settigsOnStorageJson === null) {
    return defaultSettings;
  }

  return JSON.parse(settigsOnStorageJson);
}

export const settings = (state = getSettings(), action) => {
  switch (action.type) {
    case ADD_SETTINGS:
      return { ...action.settings };
    default:
      return state;
  }
};

const users = (state = null, action) => {
  switch (action.type) {
    case ADD_USERS:
      return action.users;
    default:
      return state;
  }
};

const database = (state = null, action) => {
  switch (action.type) {
    case ADD_FIELDS:
      return action.fields;
    default:
      return state;
  }
};

const pages = (state = null, action) => {
  switch (action.type) {
    case ADD_PAGES:
      return { ...action.pages };
    default:
      return state;
  }
};


export default combineReducers({
  pages,
  request,
  database,
  structures,
  modal,
  magic,
  additives,
  users,
  settings,
});
