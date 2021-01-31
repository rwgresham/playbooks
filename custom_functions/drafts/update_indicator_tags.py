def update_indicator_tags(container_id=None, tags_to_add=None, tags_to_remove=None, replacement_tags=None, **kwargs):
    """
    Add, remove, or replace artifact tags. If using the replacement_tags input, then tags_to_add and tags_to_remove will be ignored. All tag inputs should be comma-separated lists. Any whitespace before or after the tag will be stripped.
    
    Args:
        container_id: Container ID of the artifact to update
        tags_to_add: Comma-separated list of tags to add, which will be appended to the existing list.
        tags_to_remove: Comma-separated list of tags to remove. If the artifact does not have any of these tags, they will be ignored.
        replacement_tags: Comma-separated list of tags to apply to the artifact, which will replace all tags currently applied to the artifact.
    
    Returns a JSON-serializable object that implements the configured data paths:
        
    """
    ############################ Custom Code Goes Below This Line #################################

    import json
    import phantom.rules as phantom
    
    headers = phantom.get_default_rest_headers()

    # get all tags before any changes are made
    artifact_tags_url = phantom._construct_rest_url('artifact/{}/tags'.format(artifact_id))
    response = phantom.requests.get(
        artifact_tags_url,
        verify=False,
        headers=headers
    )
    phantom.debug("phantom returned status code {} with message {}".format(response.status_code, response.text))
    tags_before = response.json()['tags']
    phantom.debug("before updating the tags on artifact with id {}, the tags are: {}".format(artifact_id, tags_before))
    
    # add the list of tags in tags_to_add
    combined_stripped_tags_to_add = []
    if tags_to_add:
        phantom.debug("adding the following new tags: {}".format(tags_to_add))
        for tag in tags_to_add.split(","):
            tag = tag.strip()
            if tag not in tags_before:
                combined_stripped_tags_to_add.append(tag.strip())
        for tag in tags_before:
            combined_stripped_tags_to_add.append(tag)

        phantom.debug("after adding new tags, the combined tags list will be: {}".format(combined_stripped_tags_to_add))
        response = phantom.requests.post(
            artifact_tags_url,
            json={'tags': combined_stripped_tags_to_add},
            verify=False,
            headers=phantom.get_default_rest_headers()
        )
        phantom.debug("phantom returned status code {} with message {}".format(response.status_code, response.text))
    
    # remove all tags in the list tags_to_remove
    if tags_to_remove:
        phantom.debug("removing the following tags: {}".format(tags_to_remove))
        remaining_tags = combined_stripped_tags_to_add
        for tag in tags_to_remove.split(","):
            stripped_tag = tag.strip()
            remaining_tags.remove(stripped_tag)

        phantom.debug("after removing tags, the combined tags list will be: {}".format(remaining_tags))
        response = phantom.requests.post(
            artifact_tags_url,
            json={'tags': remaining_tags},
            verify=False,
            headers=phantom.get_default_rest_headers()
        )
        phantom.debug("phantom returned status code {} with message {}".format(response.status_code, response.text))
    
    # finally replace all existing tags with the replacement_tags list, which will override all other tags
    if replacement_tags:
        replacement_tag_list = []
        for tag in replacement_tags.split(','):
            replacement_tag_list.append(tag.strip())
        phantom.debug("replacing all tags with {}".format(replacement_tag_list))
        response = phantom.requests.post(
            phantom._construct_rest_url('artifact/{}'.format(artifact_id)),
            verify=False,
            data=json.dumps({'tags': replacement_tag_list}),
            headers=phantom.get_default_rest_headers()
        )
    
    outputs = {}
        
    # Return a JSON-serializable object
    assert json.dumps(outputs)  # Will raise an exception if the :outputs: object is not JSON-serializable
    return outputs