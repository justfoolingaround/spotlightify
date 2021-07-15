import React, {createContext, useContext, useReducer} from "react";
import {ISuggestion} from "../types";

interface AppContext {
  suggestions: ISuggestion[]
}

export enum AppActionType {
  SET_SUGGESTIONS
}

interface ActionProps {
  type: AppActionType,
  payload?: any
}

export const reducer = (state: AppContext, action: ActionProps) => {
  switch (action.type) {
    case AppActionType.SET_SUGGESTIONS:
      if (action.payload)
        return {...state, suggestions: action.payload};

      return {...state, open: false};


    default:
      return state;
  }
};

interface ContextProps {
  state: AppContext,
  dispatch?: React.Dispatch<ActionProps>
}

const defaultState: AppContext = {
  suggestions: []
};

const Context = createContext<ContextProps>({state: defaultState});

interface AppProviderProps {
  children?: React.ReactNode
}

export const AppProvider = (props: AppProviderProps) => {
  const [state, dispatch] = useReducer(reducer, defaultState);

  return (
    <Context.Provider value={{state, dispatch}} children={props.children}/>
  )
};

export const useAppContext = () => useContext(Context);
