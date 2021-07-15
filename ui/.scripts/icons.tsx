// @ts-nocheck
import {readdirSync, readFileSync, writeFile, unlinkSync} from "fs";
import {join, extname} from "path";
import {parse as parseSvg} from "svgson";

interface INode {
	name: string,
	type: string,
	value: string,
	attributes: object,
	children: INode[]
}

interface IIconName {
	camel: string,
	hyphen: string
}

interface IIcon {
	name: IIconName,
	viewBox: string,
	element: INode[]
}

interface IIconList {
	[key: string]: IIcon
}

// this script creates src/components/icon/list.tsx

const buildNameObj = (str: string) => {
	const capitaliseFirst = (str: string) => {
		return str.charAt(0).toUpperCase() + str.slice(1);
	};

	str = str.replace(".svg", "").toLowerCase();
	const words = str.split(/\W/g);
	const hyphen = words.join("-");
	const firstWord = words.shift();

	const name: IIconName = {
		camel: firstWord + words.map(capitaliseFirst).join(""),
		hyphen
	};

	return name;
};

const clean = (obj: object) => {
	const cleaned = JSON.stringify(obj, null, 4);
	return cleaned.replace(/^[\t ]*"[^:\n\r]+(?<!\\)":/gm, match => {
		return match.replace(/"/g, "");
	});
};

const template = (content: IIconList) => {
	const iconList = clean(content);

	const result = Object.keys(content).map(key => `"${key}"`);

	const iconsType = `${result.join(" |\n\t")}`;
	const iconsArray = `[\n\t${result.join(",\n\t")}\n]`;

	return `import {IIconList} from "./interfaces";

export const iconList: IIconList = ${iconList};

export type ValidIcons = ${iconsType};

export const validIcons: string[] = ${iconsArray};
`;
};

const baseDir = __dirname.replace("\\.scripts", "");
const iconDir = join(baseDir, "assets", "svg");
const listPath = join(baseDir, "src", "components", "icon", "list.tsx");

const createList = () => {
	return new Promise<IIconList>(resolve => {
		const iconList: IIconList = {};
		const allFiles: string[] = readdirSync(iconDir).filter((file: string) => extname(file) === '.svg');

		allFiles.forEach(file => {
			const filePath = join(iconDir, file);
			const fileData = readFileSync(filePath).toString();
			const name = buildNameObj(file);

			parseSvg(fileData).then((result: any) => {
				const {attributes, children} = result;
				const {viewBox} = attributes;

				iconList[name.camel] = {
					name,
					viewBox,
					element: children
				};
			}).catch((error: any) => {
				// console.error("error", error);
			});
		});

		resolve(iconList);
	});
};

createList().then((data: IIconList) => {
	try {
		unlinkSync(listPath);
	} catch (e) {
		console.error("error", e);
	}
	writeFile(listPath, template(data), error => {
		if (error) {
			console.error("error", error);
			return;
		}
		console.info("Icons generated");
	});
});
