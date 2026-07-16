import json

from backend.engine.matrix.Base.BaseMatrix import (
    BaseMatrix,
)

from backend.project.services.models import (
    CategoryAssignmentRule,
    Service,
)

from backend.project.tickets.models import (
    TicketCategory,
)


class ServiceAutoassignMatrix(BaseMatrix):

    # =====================================================
    # META
    # =====================================================

    class Meta:

        code = (
            "service.autoassign"
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def build_schema(
        self,
        request,
    ):

        return {

            "type":
                "autoassign",

            "columns": [

                {

                    "key":
                        "executors",

                    "label":
                        "Исполнители",

                    "widget":
                        "entity_multiselect",

                    "entity":
                        "user",
                },

                {

                    "key":
                        "executor_groups",

                    "label":
                        "Группы",

                    "widget":
                        "entity_multiselect",

                    "entity":
                        "executor_group",
                },

                {

                    "key":
                        "watchers",

                    "label":
                        "Наблюдатели",

                    "widget":
                        "entity_multiselect",

                    "entity":
                        "user",
                },

            ],

        }

    # =====================================================
    # DATA
    # =====================================================

    def load_data(
        self,
        request,
    ):

        # =================================================
        # CTX
        # =================================================

        ctx_raw = request.GET.get(
            "ctx"
        )

        ctx = (
            json.loads(ctx_raw)
            if ctx_raw
            else {}
        )

        service_id = ctx.get(
            "service"
        )

        if not service_id:

            raise ValueError(
                "service is required"
            )

        # =================================================
        # SERVICE
        # =================================================

        service = (
            Service.objects
            .get(
                id=service_id
            )
        )

        # =================================================
        # CATEGORIES
        # =================================================

        categories = (

            TicketCategory.objects

            .filter(
                services=service,
            )

            .distinct()

            .order_by(
                "name"
            )

        )

        # =================================================
        # RULES
        # =================================================

        rules = {

            r.category_id: r

            for r in (

                CategoryAssignmentRule.objects

                .filter(
                    service=service,
                )

                .prefetch_related(

                    "executors",

                    "executor_groups",

                    "watchers",
                )

            )

        }

        # =================================================
        # RESULT
        # =================================================

        return {

            "layout": {

                "x": [

                    {

                        "id":
                            "executors",

                        "label":
                            "Исполнители",
                    },

                    {

                        "id":
                            "executor_groups",

                        "label":
                            "Группы",
                    },

                    {

                        "id":
                            "watchers",

                        "label":
                            "Наблюдатели",
                    },

                ],

                "y": [

                    {

                        "id":
                            str(c.id),

                        "label":
                            c.name,
                    }

                    for c in categories

                ],

            },

            "cells": {

                f"{c.id}:executors": {

                    "value": list(

                        (
                            rules.get(c.id)
                            .executors
                            .values_list(
                                "id",
                                flat=True,
                            )
                        )

                        if rules.get(c.id)
                        else []

                    )

                }

                for c in categories

            }

            |

            {

                f"{c.id}:executor_groups": {

                    "value": list(

                        (
                            rules.get(c.id)
                            .executor_groups
                            .values_list(
                                "id",
                                flat=True,
                            )
                        )

                        if rules.get(c.id)
                        else []

                    )

                }

                for c in categories

            }

            |

            {

                f"{c.id}:watchers": {

                    "value": list(

                        (
                            rules.get(c.id)
                            .watchers
                            .values_list(
                                "id",
                                flat=True,
                            )
                        )

                        if rules.get(c.id)
                        else []

                    )

                }

                for c in categories

            },

        }

    # =====================================================
    # SAVE
    # =====================================================

    def save_changes(
        self,
        request,
        changes,
    ):

        # =================================================
        # CTX
        # =================================================

        ctx_raw = request.GET.get(
            "ctx"
        )

        ctx = (
            json.loads(ctx_raw)
            if ctx_raw
            else {}
        )

        service_id = ctx.get(
            "service"
        )

        service = (
            Service.objects
            .get(
                id=service_id
            )
        )

        # =================================================
        # SAVE
        # =================================================

        for change in changes:

            category_id = change["y"]

            column = change["x"]

            value = (
                change.get("value")
                or []
            )

            category = (
                TicketCategory.objects
                .get(
                    id=category_id
                )
            )

            rule, _ = (

                CategoryAssignmentRule.objects

                .get_or_create(

                    service=service,

                    category=category,

                )

            )

            # =============================================
            # EXECUTORS
            # =============================================

            if column == "executors":

                rule.executors.set(
                    value
                )

            # =============================================
            # GROUPS
            # =============================================

            elif column == "executor_groups":

                rule.executor_groups.set(
                    value
                )

            # =============================================
            # WATCHERS
            # =============================================

            elif column == "watchers":

                rule.watchers.set(
                    value
                )

            rule.save()