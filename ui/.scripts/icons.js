"use strict";
exports.__esModule = true;
// @ts-nocheck
var fs_1 = require("fs");
var path_1 = require("path");
var svgson_1 = require("svgson");
// this script creates src/components/icon/list.tsx
var buildNameObj = function (str) {
    var capitaliseFirst = function (str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    };
    str = str.replace(".svg", "").toLowerCase();
    var words = str.split(/\W/g);
    var hyphen = words.join("-");
    var firstWord = words.shift();
    var name = {
        camel: firstWord + words.map(capitaliseFirst).join(""),
        hyphen: hyphen
    };
    return name;
};
var clean = function (obj) {
    var cleaned = JSON.stringify(obj, null, 4);
    return cleaned.replace(/^[\t ]*"[^:\n\r]+(?<!\\)":/gm, function (match) {
        return match.replace(/"/g, "");
    });
};
var template = function (content) {
    var iconList = clean(content);
    var result = Object.keys(content).map(function (key) { return "\"" + key + "\""; });
    var iconsType = "" + result.join(" |\n\t");
    var iconsArray = "[\n\t" + result.join(",\n\t") + "\n]";
    return "import {IIconList} from \"./interfaces\";\n\nexport const iconList: IIconList = " + iconList + ";\n\nexport type ValidIcons = " + iconsType + ";\n\nexport const validIcons: string[] = " + iconsArray + ";\n";
};
var baseDir = __dirname.replace("\\.scripts", "");
var iconDir = path_1.join(baseDir, "assets", "svg");
var listPath = path_1.join(baseDir, "src", "components", "icon", "list.tsx");
var createList = function () {
    return new Promise(function (resolve) {
        var iconList = {};
        var allFiles = fs_1.readdirSync(iconDir).filter(function (file) { return path_1.extname(file) === '.svg'; });
        allFiles.forEach(function (file) {
            var filePath = path_1.join(iconDir, file);
            var fileData = fs_1.readFileSync(filePath).toString();
            var name = buildNameObj(file);
            svgson_1.parse(fileData).then(function (result) {
                var attributes = result.attributes, children = result.children;
                var viewBox = attributes.viewBox;
                iconList[name.camel] = {
                    name: name,
                    viewBox: viewBox,
                    element: children
                };
            })["catch"](function (error) {
                // console.error("error", error);
            });
        });
        resolve(iconList);
    });
};
createList().then(function (data) {
    try {
        fs_1.unlinkSync(listPath);
    }
    catch (e) {
        console.error("error", e);
    }
    fs_1.writeFile(listPath, template(data), function (error) {
        if (error) {
            console.error("error", error);
            return;
        }
        console.info("Icons generated");
    });
});
