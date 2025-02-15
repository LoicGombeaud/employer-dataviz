import rules


@rules.predicate
def is_territory_liaison(user, employer):
    try:
        return user.territoryliaison.territory == employer.territory
    except:
        return False

@rules.predicate
def is_employer_liaison(user, employer):
    try:
        return user.employerliaison.employer == employer
    except:
        return False

is_territory_liaison_or_employer_liaison = is_territory_liaison | is_employer_liaison

rules.add_perm("employers.add_employer", is_territory_liaison)
rules.add_perm("employers.view_employer", is_territory_liaison_or_employer_liaison)
rules.add_perm("employers.change_employer", is_territory_liaison_or_employer_liaison)
rules.add_perm("employers.delete_employer", is_territory_liaison)
