export interface INode {
	name: string,
	type: string,
	value: string,
	attributes: object,
	children: INode[]
}

export interface IIconName {
	camel: string,
	hyphen: string
}

export interface IIcon {
	name: IIconName,
	viewBox: string,
	element: INode[]
}

export interface IIconList {
	[key: string]: IIcon
}
