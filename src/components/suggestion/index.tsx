import React, {FC} from "react";

import {ISuggestion} from "../../types";
import {Icon} from "../icon";

interface SuggestionProps extends ISuggestion {
}

export const Suggestion: FC<SuggestionProps> = (props) => {
	const {title, subtext, icon} = props;

	return (
		<div className="suggestion">
			{icon && <Icon type={icon}/>}
			<div className="suggestion-text">
				<h1>{title}</h1>
				{subtext && <h4>{subtext}</h4>}
			</div>
		</div>
	);
};
