# S5 — Software Testing Documentation (Report 7, section V)

Replaces section V of `report/05-software-testing-documentation.md` in the Report 7 docx only, in the
short SEP490 form of the template and the GSU26SE41 example. Test cases and results are in the two
Report 5 workbooks; images are rendered from them by `deliverables/tests/inject_report_v.py`.

## 1. Scope of Testing

| Level | In-Charge | Inputs/Time | Focus | Acceptance Criteria |
|---|---|---|---|---|
| Unit Testing | Developers | Each module, during development and in CI. | Logic of functions and services, edge cases. | All unit tests pass, no critical bugs. |
| Integration Testing | Backend developers | API and database, on every change. | API routes, permissions, data flow between services. | Modules integrate correctly, no major errors. |
| System Testing | Ngô Thành Đạt | Running system on the local Docker stack, before release. | Use case flows of each role through the API. | Every case Passed, or Pending with a reason. |
| Acceptance Testing | Supervisors and team | Release build, final review. | Main research workflow. | Supervisors accept the release. |

## 2. Test Strategy

### 2.1 Testing Types

| Objective | Technique | Completion Criteria |
|---|---|---|
| Testing the verification and validation of the units of code. | Unit testing | All unit tests pass, no critical logic errors. |
| Testing the group of integrated modules and the database. | Integration testing | Modules integrate correctly, no major integration issues. |
| Testing the whole system in real use by each role. | System testing | Main flows work, every failed case has a defect. |
| Testing that each role can only reach what it is allowed to. | Security testing | No role reaches data it must not reach. |

### 2.2 Test Levels

| Type of Tests | Unit | Integration | System | Acceptance |
|---|---|---|---|---|
| Unit testing | X | | | |
| Integration testing | | X | | |
| System testing | | | X | X |
| Security testing | X | X | X | |

### 2.3 Supporting Tools

| Purpose | Tool | Vendor/In-house | Version |
|---|---|---|---|
| Backend unit and integration testing | pytest | Open source | 8.4.2 |
| Frontend component testing | Vitest | Open source | 5.0.3 |
| System testing through the API | Python test script | In-house | 1.0 |
| Continuous integration | GitHub Actions | GitHub | Latest |

## 3. Test Plan

### 3.1 Human Resources

| Worker/Doer | Role | Specific Responsibilities/Comments |
|---|---|---|
| Uông Tuấn Vũ | Leader | Test planning, review test cases, defect triage. |
| Lê Vũ Phương Hòa | Member | Write unit and integration tests. |
| Ngô Thành Đạt | Member | Write unit tests, run system tests, write test reports. |
| Trần Phú Thịnh | Member | Write frontend tests. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
|---|---|---|---|
| Testing machine | macOS | Apple | 15 |
| Running the system | Docker | Docker | 29.1 |
| Backend runtime | Python | Python Software Foundation | 3.12 |
| Database | PostgreSQL | PostgreSQL Global Development Group | 16 |

### 3.3 Test Milestones

| Milestone Task | Start Date | End Date |
|---|---|---|
| Unit Test | 10/30/2026 | 10/30/2026 |
| Other Test Case (IT, ST) | 10/30/2026 | 10/30/2026 |

## 4. Test Cases

### 4.1 Unit Test Cases

FA26SE115_Report5_Unit Test.xlsx (40 functions, 330 test cases; one sheet per function, sheet create_project shown)

![Unit Test Cases](unit-cases)

### 4.2 System Test Cases

FA26SE115_Report5_Test Report.xlsx

![System Test Cases](system-cases)

## 5. Test Reports

### 5.1 Unit Test Report

FA26SE115_Report5_Unit Test.xlsx

![Unit Test Report](unit-statistics)

### 5.2 System Test Report

FA26SE115_Report5_Test Report.xlsx

![System Test Report](system-statistics)
