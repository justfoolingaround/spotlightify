/* eslint-disable no-plusplus */
import React, { ChangeEvent, useEffect, useState } from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { ipcRenderer } from 'electron';
import Prompt from './components/Prompt';
import Suggestion from './components/Suggestion';
import './App.global.css';

interface ISuggestion {
  title: string;
  description: string;
  icon: string;
}

const Container = () => {
  const [suggestions, setSuggestions] = useState<Array<ISuggestion>>([]);

  function handleChange(value: string) {
    // get suggestions here
    console.log(value);
    const newSuggestions = ['1', '2', '3'].map((id) => {
      return {
        title: `Title ${id}`,
        description: `Description ${id}`,
        icon: `Image Location ${id}`,
      };
    });
    setSuggestions(newSuggestions);
    ipcRenderer.send(
      'window-resize',
      60 * (newSuggestions.length + 1), // height
      540 // width
    );
  }

  function renderSuggestions() {
    const elements = suggestions.map(
      (obj: { title: string; description: string; icon: string }, index) => {
        const { title, description, icon } = obj;
        return (
          <Suggestion
            title={title}
            description={description}
            icon={icon}
            key={index} // TODO change this at some point
          />
        );
      }
    );
    if (elements.length !== 0) {
      return <div className="suggestion-container">{elements}</div>;
    }
    return <></>;
  }

  return (
    <div data-tid="container" className="main-container">
      <Prompt onChange={handleChange} />
      {renderSuggestions()}
    </div>
  );
};

export default function App() {
  return (
    <Router>
      <Switch>
        <Route path="/" component={Container} />
      </Switch>
    </Router>
  );
}
