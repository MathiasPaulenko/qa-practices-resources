"""Executable subset of the TaskFlow admin CRUD test cases (TC001-TC015 + edges).

Covers the API path of the test cases on
https://qapractices.com/test-cases/admin-dashboard-crud-test-cases/
"""
import sys

import pytest
import requests

ADMIN = {"Authorization": "Bearer ADMIN_TOKEN", "X-CSRF-Token": "csrf-token-123"}
VIEWER = {"Authorization": "Bearer VIEWER_TOKEN", "X-CSRF-Token": "csrf-token-123"}
AUTH_ONLY = {"Authorization": "Bearer ADMIN_TOKEN"}

PROJECT = "/api/v1/projects"
USER = "/api/v1/users"
TASK = "/api/v1/tasks"


def test_tc001_create_project(server):
    r = requests.post(server + PROJECT, headers=ADMIN, json={
        "name": "Project Beta", "code": "PROJ-002", "status": "active"})
    assert r.status_code == 201
    assert r.json()["code"] == "PROJ-002"
    assert r.json()["createdAt"]


def test_tc002_pagination(server):
    for i in range(30):
        requests.post(server + PROJECT, headers=ADMIN,
                      json={"name": "P%02d" % i, "code": "P-%03d" % i})
    r = requests.get(server + PROJECT + "?page=2&limit=25",
                     headers={"Authorization": "Bearer ADMIN_TOKEN"})
    assert r.json()["total"] == 31
    assert len(r.json()["data"]) == 6


def test_tc003_update_project_status(server):
    rec = requests.get(server + PROJECT + "/PROJ-001",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    r = requests.patch(server + PROJECT + "/PROJ-001", headers=ADMIN,
                       json={"status": "on_hold", "version": rec["version"]})
    assert r.status_code == 200
    assert r.json()["status"] == "on_hold"
    log = requests.get(server + "/api/v1/audit-log",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    assert log["entries"][0]["changes"]["status"]["old"] == "active"


def test_tc004_delete_project_without_tasks(server):
    requests.post(server + PROJECT, headers=ADMIN,
                  json={"name": "Project Beta", "code": "PROJ-002"})
    r = requests.delete(server + PROJECT + "/PROJ-002", headers=ADMIN)
    assert r.status_code == 200
    assert requests.get(server + PROJECT + "/PROJ-002",
                        headers={"Authorization": "Bearer ADMIN_TOKEN"}
                        ).status_code == 404


def test_tc005_create_user(server):
    r = requests.post(server + USER, headers=ADMIN, json={
        "name": "Carlos Ruiz", "email": "carlos.ruiz@taskflow.io",
        "role": "editor"})
    assert r.status_code == 201
    assert r.json()["role"] == "editor"


def test_tc006_update_user_role(server):
    rec = requests.get(server + USER + "/luis.herrera@taskflow.io",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    r = requests.patch(server + USER + "/luis.herrera@taskflow.io", headers=ADMIN,
                       json={"role": "admin", "version": rec["version"]})
    assert r.json()["role"] == "admin"


def test_tc007_deactivate_user(server):
    rec = requests.get(server + USER + "/luis.herrera@taskflow.io",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    r = requests.patch(server + USER + "/luis.herrera@taskflow.io", headers=ADMIN,
                       json={"active": False, "version": rec["version"]})
    assert r.json()["active"] is False


def test_tc008_create_task(server):
    r = requests.post(server + TASK, headers=ADMIN, json={
        "title": "Write docs", "code": "T-302", "projectCode": "PROJ-001"})
    assert r.status_code == 201
    assert r.json()["projectCode"] == "PROJ-001"


def test_tc010_update_task_status(server):
    rec = requests.get(server + TASK + "/T-301",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    r = requests.patch(server + TASK + "/T-301", headers=ADMIN,
                       json={"status": "in_progress", "version": rec["version"]})
    assert r.json()["status"] == "in_progress"


def test_tc011_delete_task(server):
    r = requests.delete(server + TASK + "/T-301", headers=ADMIN)
    assert r.status_code == 200
    assert requests.get(server + TASK + "/T-301",
                        headers={"Authorization": "Bearer ADMIN_TOKEN"}
                        ).status_code == 404


def test_tc012_bulk_delete_users(server):
    for email in ("a@taskflow.io", "b@taskflow.io", "c@taskflow.io"):
        requests.post(server + USER, headers=ADMIN,
                      json={"name": email, "email": email})
    r = requests.post(server + USER + "/bulk-delete", headers=ADMIN,
                      json={"ids": ["a@taskflow.io", "b@taskflow.io",
                                    "c@taskflow.io", "ghost@taskflow.io"]})
    assert r.status_code == 202
    assert r.json()["deleted"] == 3
    assert len(r.json()["errors"]) == 1


def test_tc013_search_projects(server):
    r = requests.get(server + PROJECT + "?search=alpha",
                     headers={"Authorization": "Bearer ADMIN_TOKEN"})
    assert r.json()["total"] == 1
    assert r.json()["data"][0]["code"] == "PROJ-001"


def test_tc015_validation_on_create(server):
    r = requests.post(server + PROJECT, headers=ADMIN,
                      json={"name": "", "code": "PROJ-010"})
    assert r.status_code == 400
    assert "Name is required" in r.json()["error"]
    r = requests.post(server + PROJECT, headers=ADMIN,
                      json={"name": "Dup", "code": "PROJ-001"})
    assert r.status_code == 409


def test_edge_delete_project_with_linked_tasks(server):
    r = requests.delete(server + PROJECT + "/PROJ-001", headers=ADMIN)
    assert r.status_code == 422
    assert "associated tasks" in r.json()["error"]


def test_edge_soft_delete_excluded_from_default_list(server):
    requests.delete(server + TASK + "/T-301", headers=ADMIN)
    r = requests.get(server + TASK,
                     headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    assert r["total"] == 0
    r = requests.get(server + TASK + "?include_deleted=true",
                     headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    assert r["total"] == 1


def test_edge_optimistic_locking(server):
    rec = requests.get(server + PROJECT + "/PROJ-001",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    requests.patch(server + PROJECT + "/PROJ-001", headers=ADMIN,
                   json={"status": "on_hold", "version": rec["version"]})
    stale = requests.patch(server + PROJECT + "/PROJ-001", headers=ADMIN,
                           json={"status": "done", "version": rec["version"]})
    assert stale.status_code == 409


def test_edge_invalid_status_enum(server):
    rec = requests.get(server + TASK + "/T-301",
                       headers={"Authorization": "Bearer ADMIN_TOKEN"}).json()
    r = requests.patch(server + TASK + "/T-301", headers=ADMIN,
                       json={"status": "invalid", "version": rec["version"]})
    assert r.status_code == 400


def test_edge_csrf_required(server):
    r = requests.post(server + PROJECT, headers=AUTH_ONLY,
                      json={"name": "NoCSRF", "code": "PROJ-010"})
    assert r.status_code == 403


def test_edge_viewer_token_cannot_write(server):
    r = requests.post(server + PROJECT, headers=VIEWER,
                      json={"name": "Nope", "code": "PROJ-010"})
    assert r.status_code == 403
    r = requests.get(server + PROJECT,
                     headers={"Authorization": "Bearer VIEWER_TOKEN"})
    assert r.status_code == 200


def test_audit_log_records_crud(server):
    requests.post(server + PROJECT, headers=ADMIN,
                  json={"name": "Audited", "code": "PROJ-009"})
    requests.delete(server + PROJECT + "/PROJ-009", headers=ADMIN)
    entries = requests.get(server + "/api/v1/audit-log",
                           headers={"Authorization": "Bearer ADMIN_TOKEN"}
                           ).json()["entries"]
    actions = [(e["action"], e["entityId"]) for e in entries]
    assert ("create", "PROJ-009") in actions
    assert ("delete", "PROJ-009") in actions


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
