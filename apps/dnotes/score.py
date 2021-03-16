"""
Score matches in a sensible way for our dear user.
"""

import re
import os
import time
import math
import pathlib
import inspect

import dcore.apps.dnotes.meta as meta

DEBUG = False


class __ScorerBase:
    def __init__(self):
        pass

    def score(self):
        raise "no implemented"

    def get_importance(self):
        return 1.0


################################################################################
# SCORERS IMPLEMENTATIONS
################################################################################


class __ScorerTitleOrTopOfDocument(__ScorerBase):
    """
    If something is on upper title: important.
    If it's in a later title: proportional to how low in document
        and what level title.
    """
    def score(self, search_query, lines, metadata, line, fullpath):
        score = 0

        # Bonus if in title, even better if towards beginning of file.
        for i, ll in enumerate(lines):
            titleMatchBonus = 0
            rmatch = re.search(search_query, ll, re.IGNORECASE)

            if rmatch is not None:
                level = _titleLevel(ll)

                multiplier_pos_in_document = 1 - (min(i, 100) / 100)
                multiplier_pos_in_document *= multiplier_pos_in_document
                titleMatchBonus = multiplier_pos_in_document * (0.5 *
                                                                (4 - level) /
                                                                4.0)

                # If match verbatim (no regex), even better!
                if search_query in ll:
                    titleMatchBonus += 0.2

            score += titleMatchBonus

        return score

    def get_importance(self):
        return 2.5


class __ScorerLinesMentions(__ScorerBase):
    def score(self, search_query, lines, metadata, line, fullpath):
        bonus = 0

        # Bonus if mentionned a lot in file.
        nmention = 0
        for l in lines:
            match = re.search(search_query, l, re.IGNORECASE)
            if match is not None:
                nmention += 1

        if nmention > 0:
            if nmention > 10:
                nmention = 10
            bonus = 5 * (nmention / 20)

        if False and DEBUG:
            fn = inspect.stack()[0][3]
            print('%s: %s' % (fn, bonus))

        return bonus

    def get_importance(self):
        return 1.0


class __ScorerInSpecificFolders(__ScorerBase):
    def score(self, search_query, lines, metadata, line, fullpath):
        score = 0

        path = os.path.split(fullpath)[0]

        # Some folder have special score.
        # /folder since /folder/ happens for last folder.
        if _isLineTitle(line):
            score += 0.2
        if '/articles' in path:
            # Improve: use os.path.commonprefix([]) and get_notes_archive_folder(), get_notes_low_folder(), ...
            score += 0.5
        if '/00_quality_b' in path:
            score -= 0.3
        if '/00_quality_c' in path:
            score -= 0.4
        if '/low' in path:
            score -= 0.4
        if '/done' in path:
            score -= 0.3

        return score


class __ScorerTagsAndUUID(__ScorerBase):
    def score(self, search_query, lines, metadata, line, fullpath):
        score = 0

        # Bonus if match any tag, LARGE bonus if match uuid.
        uuidVerifyUnique = None
        for metad in metadata:
            if re.search(search_query, metad.value, re.IGNORECASE):
                bonus = 0.1
                if metad.meta_type == 'uuid':
                    # Just sanity, uuid is meant to be unique per document.
                    assert uuidVerifyUnique is None
                    uuidVerifyUnique = metad.value
                    bonus = 0.3

                score += bonus

        return score

    def get_importance(self):
        return 1.0


class __ScorerSpecialTags(__ScorerBase):
    def score(self, search_query, lines, metadata, line, fullpath):
        score = 0

        # Some tags are granted a bonus / penalty.
        for metad in metadata:
            if metad.meta_type == 'uuid':
                score += 0.3

            if metad.meta_type == 'tag' and metad.value == 'not_important':
                score -= 0.5
            elif metad.meta_type == 'tag' and metad.value == 'temp':
                score -= 0.3
            elif metad.meta_type == 'tag' and metad.value == 'now':
                score += 0.3
            elif metad.meta_type == 'tag' and metad.value == 'important':
                score += 0.2
            elif metad.meta_type == 'tag' and metad.value == 'ztop':
                score += 0.6
            elif metad.meta_type == 'tag' and metad.value == 'ytop':
                score += 0.7
            elif metad.meta_type == 'tag' and metad.value == 'xtop':
                score += 0.8

        return score

    def get_importance(self):
        return 1.0


class __ScorerTopLevelFolder(__ScorerBase):
    def score(self, search_query, lines, metadata, line, fullpath):
        score = 0

        # Bonus if query matches the top level folder.
        folderName = os.path.split(fullpath)[0]
        if '/' in folderName:
            folderName = folderName.split('/')[-1]
            if re.search(search_query, folderName, re.IGNORECASE):
                score = 1.0

        # Future: might get some points for matching other folders,
        #         but less and less as goes up to notes root.

        return score

    def get_importance(self):
        return 1.0


class __ScorerLastModifiedTime(__ScorerBase):
    """
    Something modified more recently is more relevant.
    """
    def score(self, search_query, lines, metadata, line, fullpath):
        lastModified = _lastModified(fullpath)
        distFromNowDays = (time.time() - lastModified) / (60 * 60 * 24)
        assert distFromNowDays >= 0

        # solve for: e^(-x*365) = 0.5 -> -math.log(0.5)/365
        # this means that:
        # - an item modified a year ago gets a score of 0.5.
        # - an item modified today gets a score of 1.0.
        score = math.exp(-0.0018990333713971104 * distFromNowDays)

        # enforce stable sort by inserting consistent but very small
        # score based on name
        t = 1
        for c in fullpath:
            t = (t * 7 + ord(c)) % 2**30 + 0.0001
        score += 1 / t

        return score

    def get_importance(self):
        return 1.0

class __ScorerFilename(__ScorerBase):
    """
    Adjust score based on the note file.
    """
    def score(self, search_query, lines, metadata, line, fullpath):
        _, filename = os.path.split(fullpath)

        if 'meh' in filename:
            return -1.0

        return 0

    def get_importance(self):
        return 1.0


################################################################################
# UTILS
################################################################################


def _lastModified(filename):
    mtime = pathlib.Path(filename).stat().st_mtime
    return mtime


def _isLineTitle(line):
    if len(line) > 1 and line[0] == '#':
        return True
    return False


def _titleLevel(line):
    """
    titleLevel("# a title") -> 1
    titleLevel("## a title") -> 2
    titleLevel("### a title") -> 3
    titleLevel("#### a title") -> 4
    titleLevel("no markdown title") -> 0
    """

    level = 0
    if len(line) >= 1 and line[0] == '#':
        level += 1
    if len(line) >= 2 and line[1] == '#':
        level += 1
    if len(line) >= 3 and line[2] == '#':
        level += 1
    if len(line) >= 4 and line[3] == '#':
        level += 1

    assert level <= 4
    return level


################################################################################
# PUBLIC API
################################################################################


def score(match, search_query, is_explain):

    if DEBUG:
        print('scoring file: ', match.filename)

    scorers = []
    # Content
    scorers.append(__ScorerTitleOrTopOfDocument())
    scorers.append(__ScorerLinesMentions())
    # Tags
    scorers.append(__ScorerTagsAndUUID())
    scorers.append(__ScorerSpecialTags())
    # Filename
    scorers.append(__ScorerFilename())
    # Folders
    scorers.append(__ScorerInSpecificFolders())
    scorers.append(__ScorerTopLevelFolder())
    # Time
    scorers.append(__ScorerLastModifiedTime())

    with open(match.filename) as fh:
        lines = fh.readlines()

    # extract metadata
    metadata = meta.extract("\n".join(lines))

    total_score = 0
    explanation = []
    if is_explain:
        explanation = [match.filename]
    for scorer in scorers:
        score = scorer.score(search_query, lines, metadata, match.line,
                             match.filename)

        if is_explain:
            explanation.append("%s, %s, weight: %.2f" % ("{:6.2f}".format(
                score * scorer.get_importance()), scorer.__class__.__name__, scorer.get_importance()))

        # Bound. Eventually, warn if it's out of bound...
        if score < -1.0:
            score = -1.0
        if score > 1.0:
            score = 1.0

        if False and is_explain:
            explanation.append("%s, %s" % ("{:6.2f}".format(
                score * scorer.get_importance()), scorer.__class__.__name__))
        total_score += score * scorer.get_importance()

    return total_score, "\n".join(explanation)
