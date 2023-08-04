/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CharacterSchema } from '../models/CharacterSchema';
import type { CreateCharacterSchema } from '../models/CreateCharacterSchema';
import type { ListCharacterSchema } from '../models/ListCharacterSchema';
import type { UpdateCharacterSchema } from '../models/UpdateCharacterSchema';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class CharacterService {

    /**
     * List Characters
     * List all characters.
     *
     * The returned payload will not include the character sheet details.
     * @returns ListCharacterSchema Successful Response
     * @throws ApiError
     */
    public static listCharacters(): CancelablePromise<Array<ListCharacterSchema>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/character/',
        });
    }

    /**
     * Get Character
     * Returns all details of a given character.
     * @param slug
     * @returns CharacterSchema Successful Response
     * @throws ApiError
     */
    public static getCharacter(
        slug: string,
    ): CancelablePromise<CharacterSchema> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/character/{slug}',
            path: {
                'slug': slug,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Character
     * Update a character details.
     *
     * Examples of JSON body paylods:
     *
     * - `{"level": 5 }`
     * - `{"name": "Toto"}`
     * - `{"class_": "Guerrier", "data": {"background": "Folk Hero"}}`
     *
     * In the last example, we update both a direct character attribute
     * as well as an attribute nested in the character JSON data.
     * @param slug
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateCharacter(
        slug: string,
        requestBody: UpdateCharacterSchema,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}',
            path: {
                'slug': slug,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Character
     * Delete the character associated with the slug and the currently logged in player id
     * @param slug
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteCharacter(
        slug: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/character/{slug}',
            path: {
                'slug': slug,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create Character
     * Create a new character, without any data nor equipment
     * @param requestBody
     * @returns CharacterSchema Successful Response
     * @throws ApiError
     */
    public static createCharacter(
        requestBody: CreateCharacterSchema,
    ): CancelablePromise<CharacterSchema> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/character/new',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Add Item To Equipment
     * Ensure the argument item is present in the character's equipment
     * @param slug
     * @param itemId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addItemToEquipment(
        slug: string,
        itemId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}/equipment/{item_id}',
            path: {
                'slug': slug,
                'item_id': itemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Remove Item From Equipment
     * Ensure the argument item is absent from the character's equipment
     * @param slug
     * @param equippedItemId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static removeItemFromEquipment(
        slug: string,
        equippedItemId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/character/{slug}/equipment/{equipped_item_id}',
            path: {
                'slug': slug,
                'equipped_item_id': equippedItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Equip Item
     * Set the argument equipped item as equipped
     * @param slug
     * @param equippedItemId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static equipItem(
        slug: string,
        equippedItemId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}/equipment/{equipped_item_id}/equip',
            path: {
                'slug': slug,
                'equipped_item_id': equippedItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Unequip Item
     * Set the argument equipped item as unequipped
     * @param slug
     * @param equippedItemId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static unequipItem(
        slug: string,
        equippedItemId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}/equipment/{equipped_item_id}/unequip',
            path: {
                'slug': slug,
                'equipped_item_id': equippedItemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Learn Spell
     * Ensure the argument spell is added to the character's spellbook
     * @param slug
     * @param spellId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static learnSpell(
        slug: string,
        spellId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}/spellbook/{spell_id}',
            path: {
                'slug': slug,
                'spell_id': spellId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Forget Spell
     * Ensure the argument known spell is absent from the character's spellbook
     * @param slug
     * @param knownSpellId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static forgetSpell(
        slug: string,
        knownSpellId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/character/{slug}/spellbook/{known_spell_id}',
            path: {
                'slug': slug,
                'known_spell_id': knownSpellId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Prepare Spell
     * Set the argument known spell as prepared
     * @param slug
     * @param knownSpellId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static prepareSpell(
        slug: string,
        knownSpellId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}/spellbook/{known_spell_id}/prepare',
            path: {
                'slug': slug,
                'known_spell_id': knownSpellId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Unprepare Spell
     * Set the argument known spell as unprepared
     * @param slug
     * @param knownSpellId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static unprepareSpell(
        slug: string,
        knownSpellId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/character/{slug}/spellbook/{known_spell_id}/unprepare',
            path: {
                'slug': slug,
                'known_spell_id': knownSpellId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
