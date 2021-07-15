import React, {createContext, useContext, useReducer} from "react";
import {ipcRenderer} from "electron";

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
			if (action.payload) {
				const suggestions = action.payload;
				ipcRenderer.send(
					"window-resize",
					{
						width: 540,
						height: 60 * (suggestions.length + 1)
					}
				);
				return {...state, suggestions};
			}
			break;

		default:
			return state;
	}

	return state;
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

export const useAppContext = () => {
	const {state, dispatch: dispatchAction} = useContext(Context);

	// gets around needing to check if dispatch is defined every usage
	const dispatch = (action: ActionProps) => {
		if (dispatchAction) dispatchAction(action);
	};

	return {state, dispatch};
};
