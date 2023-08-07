/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { SpellCastingFocusType } from './SpellCastingFocusType';
import type { WeaponCategory } from './WeaponCategory';
import type { WeaponType } from './WeaponType';

export type ItemAttributes = {
    weapon_category: WeaponCategory;
    weapon_type: (WeaponType | null);
    ammo_type: (string | null);
    spellcasting_focus_type: (SpellCastingFocusType | null);
    range: (string | null);
};

