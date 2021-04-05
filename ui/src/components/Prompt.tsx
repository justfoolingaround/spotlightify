/* eslint-disable @typescript-eslint/ban-types */
/* eslint-disable prettier/prettier */
import React from 'react';

const Input = (props: {onChange: Function}) => {
      return (
      <input
        className="prompt-input"
        id="search"
        type="text"
        placeholder="Spotlightify Search"
        onChange={(e) => props.onChange(e.target.value)}
      />
    );
};

const Logo = () => {
  return (
    <img src="../assets/spotify-logo.svg" alt="Spotify Icon" className="logo" />
  )
}

const Prompt = (props: {onChange: Function}) => {
  return (
    <div className="prompt-container">
      <Logo />
      <Input
        onChange={(value: string) => {
          props.onChange(value);
        }}
      />
    </div>
  )
}


export default Prompt;