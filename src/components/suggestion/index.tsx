import React, { FC, ReactNode } from "react";

import { ISuggestion } from "../../types";
import { Icon } from "../icon";

interface SuggestionProps extends ISuggestion {
}

export const Suggestion: FC<SuggestionProps> = (props) => {
	const { title, subtext, icon } = props;

	return (
		<div className="suggestion">
			<div className="suggestion-icon">
				{icon && <Icon type={icon}/>}
			</div>
			<div className="suggestion-text">
				<h1>{title}</h1>
				{subtext && <h4>{subtext}</h4>}
			</div>
		</div>
	);
};

interface SuggestionContainerProps {
	children?: ReactNode
}

export const SuggestionContainer: FC<SuggestionContainerProps> = (props) => (
	<div className="suggestion-container">
		{props.children}
	</div>
);
