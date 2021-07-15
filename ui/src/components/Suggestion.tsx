import React from "react";
import {ISuggestion} from "../types";

function SuggestionTitle(props: { value: string }) {
	const {value} = props;
	return <div className="suggestion-title">{value}</div>;
}

function SuggestionDescription(props: { value: string }) {
	const {value} = props;
	return <div className="suggestion-description">{value}</div>;
}

function SuggestionIcon(props: { value: string }) {
	const {value} = props;

	return (
		<img src={`../assets/spotify.svg`} alt={value} className="suggestion-icon"/>
	);
}

function Suggestion(props: ISuggestion) {
	const {icon, title, subtext} = props;

	return (
		<div className="suggestion">
			{icon && <SuggestionIcon value={icon}/>}
			<div className="suggestion-text-container">
				<SuggestionTitle value={title}/>
				{subtext && <SuggestionDescription value={subtext}/>}
			</div>
		</div>
	);
}

export default Suggestion;
