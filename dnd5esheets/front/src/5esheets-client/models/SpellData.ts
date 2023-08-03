/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AbilityName } from './AbilityName';
import type { SpellCasting } from './SpellCasting';
import type { SpellDuration } from './SpellDuration';
import type { SpellMeta } from './SpellMeta';
import type { SpellRange } from './SpellRange';
import type { SpellScalingLevel } from './SpellScalingLevel';
import type { SpellSource } from './SpellSource';
import type { SpellTime } from './SpellTime';

export type SpellData = {
    source: SpellSource;
    casting: SpellCasting;
    meta: SpellMeta;
    time: Array<SpellTime>;
    range: SpellRange;
    duration: Array<SpellDuration>;
    misc_tags?: Array<string>;
    area_tags?: Array<string>;
    scaling_level_dice?: SpellScalingLevel;
    damage_inflict?: Array<string>;
    saving_throw?: Array<string>;
    condition_inflict?: Array<string>;
    affects_creature_type?: Array<string>;
    spell_attack?: Array<string>;
    ability_check?: Array<AbilityName>;
    damage_resist?: Array<string>;
    condition_immune?: Array<string>;
    damage_vulnerable?: Array<string>;
    damage_immune?: Array<string>;
};

