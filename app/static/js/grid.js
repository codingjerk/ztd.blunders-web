var grid = {};

(function (module) {
    var generateCaption = function(caption, cellsInRow) {
        return '<tr class="caption-row"><td class="caption-block" colspan="{0}">{1}</td></tr>'
            .format(cellsInRow, caption);
    }

    var generateNamedRow = function(rowData, cellsInRow) {
        return '<tr class="wide-row"><td class="wide-block-wrapper" colspan="{0}"><div id="{1}"></div></td></tr>'
            .format(cellsInRow, rowData.id);
    }

    var generateCell = function(cell, cellsInRow) {
        var cellSize = 100 / cellsInRow;
        return ('<td class="cell-block" style="width: {0}%;">' +
            '<div class="cell-label">{1}</div>' +
            '<div class="cell-value" id="{2}"></div>' +
            '<div class="cell-additional">{3}</div>' +
            '</td>').format(cellSize, cell.label, cell.id, cell.additional);
    }

    var parseNamedRows = function(rowsData, cellsInRow) {
        return rowsData.shiftWhile(function(row){
            return (row.type === 'chart');
        }).map(generateNamedRow, cellsInRow).join('');
    }

    var parseCells = function(rowsData, cellsInRow) {
        var cells = rowsData.shiftWhile(function(row) {
            return (row.type === 'cell');
        }).map(generateCell, cellsInRow);

        var result = '';
        while (cells.length > 0) {
            var group = cells.shiftGroup(cellsInRow).map(function(e) {return e || '';});
            result += '<tr class="short-row">' + group.join('') + '</tr>';
        }

        return result;
    }

    var generateRows = function(rowsData, cellsInRow) {
        var result = '';
        while (rowsData.length > 0) {
            result += parseNamedRows(rowsData, cellsInRow);
            result += parseCells(rowsData, cellsInRow);
        }

        return result;
    }

    var generateBlock = function(block, cellsInRow) {
        var caption = generateCaption(block.caption, cellsInRow);
        var body = generateRows(block.rows, cellsInRow);

        return '<table class="details-block">{0}{1}</table>'.format(caption, body);
    }

    module.generate = function(blocks, cellsInRow) {
        var cellsInRow = cellsInRow || 3;

        return blocks.map(generateBlock, [cellsInRow]).join('');
    }

    module.update = function(data, rules) {
        var rules = rules || {};

        for (var id in data) {
            if (rules[id] !== undefined) {
                rules[id](id, data[id]);
            } else {
                $('#' + id).html(data[id]);
            }
        };
    }
})(grid);