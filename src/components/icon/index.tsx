import React, {FC} from "react";
import classNames from "classnames";

import {genId} from "../../utils";
import {IIcon, INode} from "./interfaces";
import {iconList, ValidIcons} from "./list";

import "./icon.global.scss";

interface IconProps {
	type: ValidIcons,
	size?: "small" | "medium" | "large"
}

export const Icon: FC<IconProps> = (props) => {
	const icon: IIcon = iconList[props.type];
	const {name, viewBox, element} = icon;
	const {size} = props;

	const classes = classNames("icon", {
		"icon-s": size === "small",
		"icon-m": !size || size === "medium",
		"icon-l": size === "large",
	}, `icon-${name.hyphen}`);

	return (
		<svg className={classes} viewBox={viewBox}>
			{renderChildNodes(element)}
		</svg>
	);
};

const renderChildNodes = (nodes: INode[]) => {
	return (
		<>
			{nodes.map(child => {
				const {name, attributes, children} = child;
				const Tag = name.toString();

				// @ts-ignore
				return <Tag key={genId()} {...attributes}>{renderChildNodes(children)}</Tag>
			})}
		</>
	)
};
