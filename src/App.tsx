/* eslint-disable no-plusplus */
import React from "react";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";

import {AppActionType, AppProvider, useAppContext} from "./context";
import {ISuggestion} from "./types";

import {Prompt} from "./components/prompt";
import {Suggestion} from "./components/suggestion";

import "./App.global.css";

const Container = () => {
	const {state, dispatch} = useAppContext();

	const handleChange = (value: string) => {
		// get suggestions here
		let newSuggestions: ISuggestion[] = [];

		if (value.length > 0) {
			newSuggestions = ["1", "2", "3"].map((id) => {
				return {
					title: `Title ${id}`,
					subtext: `Description ${id}`,
					icon: "album",
				};
			});
		}

		dispatch({
			type: AppActionType.SET_SUGGESTIONS,
			payload: newSuggestions
		});
	};

	return (
		<div data-tid="container" className="main-container">
			<Prompt onChange={handleChange}/>
			{state.suggestions.map((item: ISuggestion, index) => (
				<Suggestion key={index} {...item}/>
			))}
		</div>
	)
};

export const App = () => {
	return (
		<AppProvider>
			<Router>
				<Switch>
					<Route path="/" component={Container}/>
				</Switch>
			</Router>
		</AppProvider>
	);
};
