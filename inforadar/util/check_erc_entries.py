import tldextract

from inforadar.models import ErcSource, ErcSourceSchema


def is_registered_domain(article_url):
    # Check if URL subdomain (or domain) belongs to a verified source.
    ext = tldextract.extract(article_url)
    domain = "{}.{}".format(ext.domain, ext.suffix)
    subdomain = "{}.{}.{}".format(ext.subdomain, ext.domain, ext.suffix).replace("www.", "")

    erc_source_subdomain = ErcSource.query.filter_by(domain=subdomain).first()
    erc_source_domain = ErcSource.query.filter_by(domain=domain).first()

    if erc_source_subdomain:
        # print(erc_source_subdomain.title, erc_source_subdomain.registration_number)
        # Serialize the data for the response
        erc_source_schema = ErcSourceSchema(many=False)
        erc_source_data = erc_source_schema.dump(erc_source_subdomain)
        return erc_source_data

    elif erc_source_domain:
        # print(erc_source_domain.title, erc_source_domain.registration_number)
        # Serialize the data for the response
        erc_source_schema = ErcSourceSchema(many=False)
        erc_source_data = erc_source_schema.dump(erc_source_domain)
        return erc_source_data
    # Subdomain and domain not found.
    return {}
