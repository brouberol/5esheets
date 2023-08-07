/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ItemAttributes } from './ItemAttributes';
import type { ItemDamage } from './ItemDamage';
import type { ResourceTranslation } from './ResourceTranslation';

export type ItemMeta = {
    translations: (Record<string, ResourceTranslation> | null);
    rarity: string;
    weight: (number | null);
    value: number;
    attributes: (ItemAttributes | null);
    damage: (ItemDamage | null);
    property: (Array<string> | null);
    effect: (string | null);
    requirements: (Record<string, any> | null);
    stealth: (boolean | null);
};

