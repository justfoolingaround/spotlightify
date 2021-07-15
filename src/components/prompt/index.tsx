import React, {FC} from "react";
import classNames from "classnames";

import {Icon} from "../icon";

import "./prompt.scss";

interface PromptProps {
	onChange(value: string): void
}

export const Prompt: FC<PromptProps> = (props) => {
	const classes = classNames("prompt");

	return (
		<div className={classes}>
			<Icon type="spotify" size="large"/>
			<input onChange={e => props.onChange(e.target.value)}/>
		</div>
	)
};
