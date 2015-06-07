var grid = {};

(function (module) {
    var generateCaption = function(caption) {
        return '<tr class="caption-row"><td class="caption-block" colspan="3">{0}</td></tr>'
            .format(caption);
    }

    var generateNamedRow = function(rowData) {
        return '<tr class="info-row"><td class="info-block-wrapper" colspan="3"><div id="{0}"></div></td></tr>'
            .format(rowData.id);
    }

    var generateCell = function(cell) {
        return ('<td class="grid-block">' +
            '<div class="grid-label">{0}</div>' +
            '<div class="grid-value" id="{1}"></div>' +
            '<div class="grid-additional">{2}</div>' +
            '</td>').format(cell.label, cell.id, cell.additional);
    }

    var generateRow = function(rowData) {
        if (rowData.type === 'cell') {
            return generateCell(rowData);
        } else if (rowData.type === 'chart') {
            return generateNamedRow(rowData);
        }

        console.log('grid.generateRow: Unknown row type');
    }

    var parseNamedRows = function(rowsData) {
        return rowsData.shiftWhile(function(row){
            return (row.type === 'chart');
        }).map(generateRow).join('');
    }

    var parseCells = function(rowsData) {
        var cells = rowsData.shiftWhile(function(row) {
            return (row.type === 'cell');
        }).map(generateRow);

        var result = '';
        while (cells.length > 0) {
            var group = cells.shiftGroup(3).map(function(e) {return e || '';});
            result += '<tr class="grid-row">' + group.join('') + '</tr>';
        }

        return result;
    }

    var generateRows = function(rowsData) {
        var result = '';
        while (rowsData.length > 0) {
            result += parseNamedRows(rowsData);
            result += parseCells(rowsData);
        }

        return result;
    }

    var generateBlock = function(block) {
        var caption = generateCaption(block.caption);
        var body = generateRows(block.rows);

        return '<table class="details-block">{0}{1}</table>'.format(caption, body);
    }

    module.generate = function(blocks) {
        return blocks.map(generateBlock).join('');
    }

    module.update = function(data, rules) {
        var rules = rules || {};

        data.map(function(element) {
            var ruleFunction = rules[element.id];

            if (ruleFunction !== undefined) {
                ruleFunction(element.id, element.value);
            } else {
                $('#' + element.id).html(element.value);
            }
        });
    }
})(grid);