import React from 'react';

function SuggestionTitle(props: { value: string }) {
  const { value } = props;
  return <div className="suggestion-title">{value}</div>;
}

function SuggestionDescription(props: { value: string }) {
  const { value } = props;
  return <div className="suggestion-description">{value}</div>;
}

function SuggestionIcon(props: { value: string }) {
  const { value } = props;

  return (
    <img src={`../assets/spotify-logo.svg`} alt={value} className="suggestion-icon" />
  );
}

function Suggestion(props: {
  title: string;
  description: string;
  icon: string;
}) {
  const { icon, title, description } = props;

  return (
    <div className="suggestion">
      <SuggestionIcon value={icon} />
      <div className="suggestion-text-container">
        <SuggestionTitle value={title} />
        <SuggestionDescription value={description} />
      </div>
    </div>
  );
}

export default Suggestion;
