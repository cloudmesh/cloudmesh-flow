# ISO 27000 standards

The ISO 27000 family of standards deal with information security. Most cloud vendors incorporate ISO 27000 compliance into their overall security strategy. The standard defines the requirements for an information security management system (ISMS) including how to put such a system in place, ensure that procedures are followed, and update security procedures as new threats are released. 

In 2006, the original publication defining security standards was released as ISO 27001. Over the next few years, security analysts and researchers argued that while the 27001 standard was a good start, the requirements it laid out were inadequate to meet the security demands of a large organization. As a result, ISO 27001 grew into what are now referred to as the ISO 27000 (or ISO 27k) family of standards. The family was first published 2013 and the most recent revision was in 2018. 

## Contents

As with most ISO standards, the full text of the standard itself is not freely available to the public. The contents are available for purchase on the ISO [website](https://www.iso.org/obp/ui/#iso:std:iso-iec:27001:ed-2:v1:en) along with a small free sample.

A summary of the contents is as follows:

| Standard      | Description |
| ----------- | ----------- |
| ISO 27000      | Provides an overview of security requirements in the following standards, defines common terms       |
| ISO 27001   | Sets out requirements for Information Security Management Systems, including checklist for certification        |
| ISO 27002   | Lists controls to put in place and best practices to follow and manage with an ISMS|
| ISO 27003   | Offers guidance and best practices for implementing an ISMS|
| ISO 27004   | Determines how to evaluate and analyze an ISMS including monitoring and specific measurements |
| ISO 27005   | Discusses risk management and how to evaluate new risks|
| ISO 27006 - 009  | Details audit requirements, including a checklist for auditors        |
| ISO 270010 - 0018   | Implementation details and guidelines for ISMS in different contexts       |
| ISO 27033   | Network security specific guidelines        |
| ISO 27034   | Application security specific guidelines        |
| ISO 27035- 43   | Incident response & management        |

## ISO 27k In Practice

While most cloud vendors and many smaller enterprises advertise their ISO 27000 compatibility, it can be difficult to determine what that means in practice. In general, a compliant organization has a written ISMS Security Policy that implements the relevant ISO guidelines, along with both internal and external audits that ensure their compliance with the policy.

### Networking Requirements

The standard lays out very specific guidelines for networking, as well as best practices. These cover networks that are used by cloud applications, as well as in-house networks that are used by employees. Security is an "essential element" of networks, and must be incorporated as such.

For applications, networks should be hardened as much as permissible. Where possible based on application, firewalls and whitelists are recommended to limit the attack surface. Sending information in plain text without encryption is discouraged, and HTTPS/TLS is strongly encouraged.

For in-house networks, the standard recommends many best practices for ensuring that security is not compromised in trying to make a user-friendly network. Networks should be segregated, and users should be limited in what they can access without identifying themselves in a specific role. Trust based on networks is to be avoided, for example a VPN by itself is not a sufficient security solution.

### Cryptographic Requirements

Implementing good cryptography can be tricky, and ensuring you're following best practices closely is very important for complying with the standard.

In general, the best practice recommended by the standard is to encrypt as much as possible given the risk profile of the organization. There should be a documented policy to understand what information should be encrypted and how it is encrypted. Because security standards are frequently changing, organizations should document what levels of encryption to use and update those recommendations as the threat landscape changes.

Key management is also important. Documenting and understanding what to do with sensitive files like private keys is an important part of the standard. It's also important to ensure that keys are generated in a random way, and that weak keys aren't used. Because keys contain potentially sensitive information, they should be destroyed when no longer needed.


### Other Requirements

While much of the standard discusses computers and computing equipment, there are also sections devoted to human resources. It is recommended that background checks be performed on employees, and other documented screening for potential bad behaviors. Ongoing personnel training is recommended, and employees are expected to assess the security impact of their work. Finally, an auditable process for removing sensitive information from terminated employees is required.

Other recommendations cover physical site security, like ensuring only allowed personnel are allowed near equipment that might allow access to sensitive information. The ISO places an emphasis on logging for both physical hardware and software to ensure there is a document trail to detect anomalies and document past behavior.


Finally, the standard requires that the ISMS implementation be continually monitored and updated. Security requirements are constantly changing, and the standard itself changes with some frequency as the threat landscape changes. Compliant organizations must monitor for new threats, and explicitly track metrics that demonstrate their risk profile. Continual improvement is a stated goal of the standard.

