/* eslint-disable no-plusplus */
import React from "react";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import {ipcRenderer} from "electron";

import {AppActionType, AppProvider, useAppContext} from "./context";
import {ISuggestion} from "./types";

import Prompt from "./components/Prompt";
import Suggestion from "./components/Suggestion";
import "./App.global.css";


const Container = () => {
  const {state, dispatch} = useAppContext();

  function handleChange(value: string) {
    // get suggestions here
    console.log(value);
    const newSuggestions = ["1", "2", "3"].map((id) => {
      return {
        title: `Title ${id}`,
        subtext: `Description ${id}`,
        icon: `Image Location ${id}`,
      };
    });

    if (dispatch)
      dispatch({
        type: AppActionType.SET_SUGGESTIONS,
        payload: newSuggestions
      });

    ipcRenderer.send(
      "window-resize",
      60 * (newSuggestions.length + 1), // height
      540, // width,
      screen
    );
  }

  return (
    <div data-tid="container" className="main-container">
      <Prompt onChange={handleChange}/>
      {state.suggestions.map((item: ISuggestion, index) => (
        <Suggestion key={index} {...item}/>
      ))}
    </div>
  )
};

export default function App() {
  return (
    <AppProvider>
      <Router>
        <Switch>
          <Route path="/" component={Container}/>
        </Switch>
      </Router>
    </AppProvider>
  );
}
