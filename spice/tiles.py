from math import ceil
from flask import Blueprint, render_template, g

from . import util

bp = Blueprint("tiles", __name__, url_prefix="/tiles")


class Tile:
    def __init__(self, image, span):
        self.span = span
        self.file = image
        self.adjusted = False


def get_width(f):
    if f.size["width"] > 200:
        return min(4, ceil(f.size["width"] / f.size["height"]))
    return 1


def find(files, maxSize):
    for idx, f in enumerate(files):
        if get_width(f) <= maxSize:
            return idx
    return None


def sort(files):
    cols = 8
    row = 0
    tiles = []

    images = [f for f in files if f.type == "images"]
    count = 500

    while len(images) and count != 0:
        count -= 1
        index = find(images, cols - row)
        if index is None:
            if row == 0:
                f = images.pop(0)
                width = get_width(f)
                print(
                    "adding {} {} {}".format(width, f.size["width"], f.size["height"])
                )
                tiles.append(Tile(f, width))
            else:
                print("Fitting short row {}".format(row))
                extra = cols - row
                tile_count = 0
                idx = -1
                while row > 0:
                    tile_count += 1
                    row -= tiles[idx].span
                    idx -= 1

                if extra // tile_count:
                    print(
                        "padding tiles {} {} {}".format(
                            extra, tile_count, extra // tile_count
                        )
                    )
                    while idx != -1:
                        tiles[idx].span += extra // tile_count
                        tiles[idx].adjusted = True
                        idx += 1
                    tiles[-1].span += ceil(extra / tile_count)
                    tiles[-1].adjusted = True
                else:
                    print("last tile gets all {} {}".format(tiles[-1].span, extra))
                    tiles[-1].span += extra
                    tiles[-1].adjusted = True

                row = 0
        else:
            f = images.pop(index)
            width = get_width(f)
            tiles.append(Tile(f, width))
            row += width

        if row == cols:
            row = 0
    if count == 0:
        print("Aborted sort, iteration max hit")
    return tiles


@bp.route("/")
@bp.route("/<int:page>")
def tile(page=0):
    page_size = 56
    json, files = util.get_file_data(page_size, page * page_size)

    next_page = False
    if len(files) == page_size:
        next_page = page + 1

    return render_template(
        "tiles.html",
        current_user=g.user,
        files=sort(files),
        json=json,
        view="tiles.tile",
        prev_page=page - 1,
        next_page=next_page,
    )
